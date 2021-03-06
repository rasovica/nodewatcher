# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-03-24 13:17
from __future__ import unicode_literals

from django.db import migrations, models
import nodewatcher.core.registry.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cgm', '0019_auto_20170323_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='ethernetinterfaceconfig',
            name='routing_default_announces',
            field=nodewatcher.core.registry.fields.RegistryMultipleChoiceField(base_field=models.CharField(choices=[(b'olsr', 'OLSR HNA'), (b'babel', 'Babel')], max_length=50), blank=True, default=list, enum_id=b'core.interfaces.network#routing_announce', null=True, regpoint=b'node.config', size=None, verbose_name='Announce Default Route Via'),
        ),
        migrations.AddField(
            model_name='mobileinterfaceconfig',
            name='routing_default_announces',
            field=nodewatcher.core.registry.fields.RegistryMultipleChoiceField(base_field=models.CharField(choices=[(b'olsr', 'OLSR HNA'), (b'babel', 'Babel')], max_length=50), blank=True, default=list, enum_id=b'core.interfaces.network#routing_announce', null=True, regpoint=b'node.config', size=None, verbose_name='Announce Default Route Via'),
        ),
        migrations.AddField(
            model_name='wifiinterfaceconfig',
            name='routing_default_announces',
            field=nodewatcher.core.registry.fields.RegistryMultipleChoiceField(base_field=models.CharField(choices=[(b'olsr', 'OLSR HNA'), (b'babel', 'Babel')], max_length=50), blank=True, default=list, enum_id=b'core.interfaces.network#routing_announce', null=True, regpoint=b'node.config', size=None, verbose_name='Announce Default Route Via'),
        ),
    ]
