# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-21 04:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0006_auto_20160422_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationconfig',
            name='altitude',
            field=models.FloatField(default=0, help_text='In meters.'),
        ),
    ]
