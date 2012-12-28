import multiprocessing

from django.db import transaction, connection
from django.utils import unittest

from .allocation import pool

@transaction.commit_on_success
def _concurrent_allocation_worker(pool):
    try:
        alloc = pool.allocate_subnet(prefix_len = 27)
        alloc.free()
        alloc = pool.allocate_subnet(prefix_len = 27)
    except:
        return None

    return (alloc.network, alloc.prefix_length)

class IpPoolTestCase(unittest.TestCase):
    def setUp(self):
        """
        Prepare the IP pool test environment by creating some dummy IP
        pools.
        """
        self.pool = pool.IpPool.objects.create(
          family = "ipv4",
          network = "10.10.0.0",
          prefix_length = 16,
        )

        self.small_pool = pool.IpPool.objects.create(
          family = "ipv4",
          network = "192.168.1.0",
          prefix_length = 26,
        )

    def test_basic_allocation(self):
        # Test that we really get properly allocated objects
        a = self.pool.allocate_subnet(prefix_len = 27)
        b = self.pool.allocate_subnet(prefix_len = 27)
        c = self.pool.allocate_subnet(prefix_len = 26)

        # Test that something has been allocated
        self.assertNotEqual(a, None)
        self.assertNotEqual(b, None)
        self.assertNotEqual(c, None)

        # Test that we really have the right prefix lengths
        self.assertEqual(a.prefix_length, 27)
        self.assertEqual(b.prefix_length, 27)
        self.assertEqual(c.prefix_length, 26)

        # Test that distinct subnets have been allocated
        networks = set([a.network, b.network, c.network])
        self.assertEqual(len(networks), 3)

        # Test that statuses have been properly set
        self.assertEqual(a.status, pool.IpPoolStatus.Full)
        self.assertEqual(b.status, pool.IpPoolStatus.Full)
        self.assertEqual(c.status, pool.IpPoolStatus.Full)

    def test_allocation_failure(self):
        # Test that we can't allocate more than we have
        a = self.small_pool.allocate_subnet(prefix_len = 24)
        self.assertEqual(a, None)

        # Test that we fail to get an allocation when the pool is exhausted
        a = self.small_pool.allocate_subnet(prefix_len = 27)
        b = self.small_pool.allocate_subnet(prefix_len = 27)
        c = self.small_pool.allocate_subnet(prefix_len = 27)
        self.assertNotEqual(a, None)
        self.assertNotEqual(b, None)
        self.assertEqual(c, None)

    def test_freeing(self):
        # Test that free works as expected
        a = self.pool.allocate_subnet(prefix_len = 26)
        b = self.pool.allocate_subnet(prefix_len = 27)
        a.free()
        c = self.pool.allocate_subnet(prefix_len = 26)
        self.assertEqual(c.network, a.network)
        self.assertEqual(c.prefix_length, a.prefix_length)

    def test_concurrent_allocation(self):
        # Close the connection to avoid sharing it with child processes
        connection.close()
        # Create the worker pool
        workers = multiprocessing.Pool(10)
        NUM_REQUESTS = 100

        try:
            # Submit lots of requests and verify that all are unique and fulfilled
            allocations = set(workers.map(_concurrent_allocation_worker, [self.pool] * NUM_REQUESTS))
            self.assertEqual(len(allocations), NUM_REQUESTS)
        finally:
            workers.close()
            workers.join()
