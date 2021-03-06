# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-14 16:53
from __future__ import unicode_literals

from django.db import migrations

from .. import base as cgm_base


def migrate_ethernet_interface_names(apps, schema_editor):
    CgmGeneralConfig = apps.get_model('cgm', 'CgmGeneralConfig')
    EthernetInterfaceConfig = apps.get_model('cgm', 'EthernetInterfaceConfig')
    SwitchConfig = apps.get_model('cgm', 'SwitchConfig')
    VLANConfig = apps.get_model('cgm', 'VLANConfig')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    for general in CgmGeneralConfig.objects.all():
        if not general.router or not general.platform:
            continue

        # For each switch, generate configuration from default preset.
        try:
            device = cgm_base.get_platform(general.platform).get_device(general.router)
        except KeyError:
            continue

        for switch in device.switches:
            switch_cfg = SwitchConfig(
                polymorphic_ctype=ContentType.objects.get_for_model(SwitchConfig),
                root=general.root,
                switch=switch.identifier,
                vlan_preset='default',
            )
            switch_cfg.save()

            preset = switch.get_preset('default')
            for vlan in preset.vlans:
                # Create all VLAN configurations.
                VLANConfig(
                    polymorphic_ctype=ContentType.objects.get_for_model(VLANConfig),
                    root=general.root,
                    switch=switch_cfg,
                    vlan=vlan.vlan,
                    name=vlan.description,
                    ports=vlan.ports,
                ).save()

                # Update interfaces to new port names.
                EthernetInterfaceConfig.objects.filter(
                    root=general.root,
                    eth_port=vlan.identifier
                ).update(eth_port=switch.get_port_identifier(vlan.vlan))


class Migration(migrations.Migration):

    dependencies = [
        ('cgm', '0017_auto_20161014_1337'),
    ]

    operations = [
        migrations.RunPython(migrate_ethernet_interface_names),
    ]
