# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-13 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0074_auto_20170913_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='picture_urls',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entitylog',
            name='picture_urls',
            field=models.TextField(null=True),
        ),
    ]