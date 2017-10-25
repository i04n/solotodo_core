# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-17 12:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('solotodo', '0001_initial'),
        ('category_templates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorytemplate',
            name='api_client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solotodo.ApiClient'),
        ),
        migrations.AddField(
            model_name='categorytemplate',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solotodo.Category'),
        ),
        migrations.AddField(
            model_name='categorytemplate',
            name='purpose',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category_templates.CategoryTemplatePurpose'),
        ),
        migrations.AlterUniqueTogether(
            name='categorytemplate',
            unique_together=set([('category', 'api_client', 'purpose')]),
        ),
    ]