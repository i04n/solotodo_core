# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0023_auto_20170808_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTypeTier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('creation_payment_amount', models.DecimalField(decimal_places=0, max_digits=5)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]