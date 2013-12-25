# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RttMeasurementMonitor.rtt_std'
        db.add_column('monitor_rttmeasurementmonitor', 'rtt_std',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RttMeasurementMonitor.rtt_std'
        db.delete_column('monitor_rttmeasurementmonitor', 'rtt_std')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.generalmonitor': {
            'Meta': {'object_name': 'GeneralMonitor'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'first_seen': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monitoring_core_generalmonitor'", 'to': "orm['core.Node']"})
        },
        'core.node': {
            'Meta': {'object_name': 'Node'},
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        },
        'monitor.cgmgeneralmonitor': {
            'Meta': {'ordering': "['id']", 'object_name': 'CgmGeneralMonitor', '_ormbases': ['core.GeneralMonitor']},
            'firmware': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'generalmonitor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.GeneralMonitor']", 'unique': 'True', 'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        'monitor.generalresourcesmonitor': {
            'Meta': {'ordering': "['id']", 'object_name': 'GeneralResourcesMonitor'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loadavg_15min': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'loadavg_1min': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'loadavg_5min': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'memory_buffers': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'memory_cache': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'memory_free': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'processes': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monitoring_monitor_generalresourcesmonitor'", 'to': "orm['core.Node']"})
        },
        'monitor.interfacemonitor': {
            'Meta': {'ordering': "['id']", 'object_name': 'InterfaceMonitor'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'hw_address': ('nodewatcher.core.registry.fields.MACAddressField', [], {'max_length': '17', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtu': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monitoring_monitor_interfacemonitor'", 'to': "orm['core.Node']"}),
            'rx_bytes': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '100', 'decimal_places': '0'}),
            'rx_drops': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '100', 'decimal_places': '0'}),
            'rx_errors': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '100', 'decimal_places': '0'}),
            'rx_packets': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '100', 'decimal_places': '0'}),
            'tx_bytes': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '100', 'decimal_places': '0'}),
            'tx_drops': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '100', 'decimal_places': '0'}),
            'tx_errors': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '100', 'decimal_places': '0'}),
            'tx_packets': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '100', 'decimal_places': '0'})
        },
        'monitor.networkresourcesmonitor': {
            'Meta': {'ordering': "['id']", 'object_name': 'NetworkResourcesMonitor'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monitoring_monitor_networkresourcesmonitor'", 'to': "orm['core.Node']"}),
            'routes': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'tcp_connections': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'udp_connections': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'monitor.rttmeasurementmonitor': {
            'Meta': {'ordering': "['id']", 'object_name': 'RttMeasurementMonitor'},
            'all_packets': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'failed_packets': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'packet_loss': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'packet_size': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'monitoring_monitor_rttmeasurementmonitor'", 'to': "orm['core.Node']"}),
            'rtt_average': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rtt_maximum': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rtt_minimum': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rtt_std': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Node']", 'null': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'successful_packets': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        'monitor.wifiinterfacemonitor': {
            'Meta': {'ordering': "['id']", 'object_name': 'WifiInterfaceMonitor', '_ormbases': ['monitor.InterfaceMonitor']},
            'bitrate': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'bssid': ('nodewatcher.core.registry.fields.MACAddressField', [], {'max_length': '17', 'null': 'True'}),
            'channel': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'channel_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'essid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'frag_threshold': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'interfacemonitor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['monitor.InterfaceMonitor']", 'unique': 'True', 'primary_key': 'True'}),
            'mode': ('nodewatcher.core.registry.fields.SelectorKeyField', [], {'max_length': '50', 'null': 'True', 'regpoint': "'node.config'", 'enum_id': "'core.interfaces#wifi_mode'"}),
            'noise': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'rts_threshold': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'signal': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'snr': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        }
    }

    complete_apps = ['monitor']