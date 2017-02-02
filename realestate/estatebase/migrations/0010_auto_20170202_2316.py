# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0009_auto_20170202_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
                ('room_count', models.PositiveIntegerField(null=True, verbose_name='Room count', blank=True)),
                ('total_area_min', models.DecimalField(null=True, verbose_name='Total area min', max_digits=10, decimal_places=2, blank=True)),
                ('total_area_max', models.DecimalField(null=True, verbose_name='Total area min', max_digits=10, decimal_places=2, blank=True)),
                ('used_area_min', models.DecimalField(null=True, verbose_name='Used area min', max_digits=10, decimal_places=2, blank=True)),
                ('used_area_max', models.DecimalField(null=True, verbose_name='Used area max', max_digits=10, decimal_places=2, blank=True)),
                ('price_per_sqm_min', models.IntegerField(null=True, verbose_name='Price per sq. m. min', blank=True)),
                ('price_per_sqm_max', models.IntegerField(null=True, verbose_name='Price per sq. m. max', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'BuildingItem',
                'verbose_name_plural': 'BuildingItems',
            },
        ),
        migrations.AlterField(
            model_name='genericsupply',
            name='distance',
            field=models.PositiveIntegerField(verbose_name='Distance'),
        ),
        migrations.AlterField(
            model_name='genericsupply',
            name='supply',
            field=models.ForeignKey(verbose_name='Supply', to='estatebase.Supply'),
        ),
        migrations.AlterField(
            model_name='genericsupply',
            name='supply_state',
            field=models.ForeignKey(verbose_name='Supply state', blank=True, to='estatebase.SupplyState', null=True),
        ),
        migrations.AlterField(
            model_name='yandexbuilding',
            name='ready_year',
            field=models.IntegerField(null=True, verbose_name='Ready year', blank=True),
        ),
        migrations.AddField(
            model_name='yandexbuilding',
            name='items',
            field=models.ManyToManyField(to='estatebase.BuildingItem', null=True, blank=True),
        ),
    ]
