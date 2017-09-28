# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-25 12:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0082_auto_20170915_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreVisit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('ip', models.GenericIPAddressField()),
                ('entity_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solotodo.EntityHistory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('entity_history', 'timestamp'),
            },
        ),
        migrations.AlterModelOptions(
            name='entity',
            options={'ordering': ('creation_date',), 'permissions': [('backend_list_entities', 'Can view entity list in backend')]},
        ),
        migrations.AlterModelOptions(
            name='entitylog',
            options={'ordering': ('entity', 'creation_date')},
        ),
        migrations.AlterModelOptions(
            name='language',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='numberformat',
            options={'ordering': ('name',)},
        ),
    ]