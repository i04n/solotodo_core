# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 20:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0030_auto_20170811_1627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entity',
            options={'permissions': [('backend_list_entity', 'Can view entity list in backend')]},
        ),
    ]