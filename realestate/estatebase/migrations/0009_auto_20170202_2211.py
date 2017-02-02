# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0008_auto_20170202_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='yandexbuilding',
            name='exterior_finish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Exterior finish', blank=True, to='estatebase.ExteriorFinish', null=True),
        ),
        migrations.AddField(
            model_name='yandexbuilding',
            name='price_per_sqm_max',
            field=models.IntegerField(null=True, verbose_name='Price per sq. m. max', blank=True),
        ),
        migrations.AddField(
            model_name='yandexbuilding',
            name='price_per_sqm_min',
            field=models.IntegerField(null=True, verbose_name='Price per sq. m. min', blank=True),
        ),
        migrations.AddField(
            model_name='yandexbuilding',
            name='wall_construcion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Wall construcion', blank=True, to='estatebase.WallConstrucion', null=True),
        ),
        migrations.AddField(
            model_name='yandexbuilding',
            name='wall_finish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='WallFinish', blank=True, to='estatebase.WallFinish', null=True),
        ),
    ]
