# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 19:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0039_numberformat_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='decimal_separator',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='thousands_separator',
        ),
    ]