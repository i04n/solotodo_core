# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-14 19:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0076_auto_20170914_1606'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'permissions': (['view_category', 'Can view the category'], ['view_category_products', 'Can view products associated to this category'], ['category_entities_staff', 'Is staff of the entities of this category (also requires store permissions)'], ['update_category_entities_pricing', "Can update the pricing of this category's entities"], ['backend_view_category', 'Can view category list / detail in the backend'])},
        ),
    ]