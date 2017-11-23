# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-23 15:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0009_auto_20171114_2039'),
        ('wtb', '0005_auto_20171123_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='wtbbrand',
            name='website',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='solotodo.Website'),
            preserve_default=False,
        ),
    ]
