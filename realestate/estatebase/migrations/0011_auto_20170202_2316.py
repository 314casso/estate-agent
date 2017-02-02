# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0010_auto_20170202_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yandexbuilding',
            name='items',
            field=models.ManyToManyField(to='estatebase.BuildingItem', blank=True),
        ),
    ]
