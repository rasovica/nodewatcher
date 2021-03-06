from django.db import models as django_models

from rest_framework import mixins, viewsets

from nodewatcher.core import models as core_models

from . import serializers


class StatusStatisticsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Endpoint for global per-status statistics.
    """

    queryset = core_models.Node.objects.regpoint('monitoring').registry_fields(
        status='core.status__network'
    ).values(
        'status'
    ).annotate(
        nodes=django_models.Count('uuid')
    )
    serializer_class = serializers.StatusStatisticsSerializer
