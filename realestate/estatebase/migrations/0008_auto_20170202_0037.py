# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('estatebase', '0007_auto_20170110_2138'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericSupply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('distance', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Supply',
                'verbose_name_plural': 'Supply',
            },
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Supply',
                'verbose_name_plural': 'Supply',
            },
        ),
        migrations.CreateModel(
            name='SupplyState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Supply state',
                'verbose_name_plural': 'Supply states',
            },
        ),
        migrations.AddField(
            model_name='yandexbuilding',
            name='discount',
            field=models.TextField(null=True, verbose_name='Discount', blank=True),
        ),
        migrations.AddField(
            model_name='yandexbuilding',
            name='dummy_address',
            field=models.CharField(max_length=255, null=True, verbose_name='Dummy address', blank=True),
        ),
        migrations.AddField(
            model_name='yandexbuilding',
            name='ready_year',
            field=models.IntegerField(null=True, verbose_name='Year', blank=True),
        ),
        migrations.AddField(
            model_name='genericsupply',
            name='supply',
            field=models.ForeignKey(to='estatebase.Supply'),
        ),
        migrations.AddField(
            model_name='genericsupply',
            name='supply_state',
            field=models.ForeignKey(blank=True, to='estatebase.SupplyState', null=True),
        ),
    ]
