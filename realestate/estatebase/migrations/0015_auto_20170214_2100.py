# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0014_auto_20170209_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingitem',
            name='price_per_sqm_max',
            field=models.IntegerField(null=True, verbose_name='Price max', blank=True),
        ),
        migrations.AlterField(
            model_name='buildingitem',
            name='price_per_sqm_min',
            field=models.IntegerField(null=True, verbose_name='Price min', blank=True),
        ),
        migrations.AlterField(
            model_name='genericsupply',
            name='distance',
            field=models.PositiveIntegerField(null=True, verbose_name='Distance', blank=True),
        ),
    ]
