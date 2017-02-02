# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0011_auto_20170202_2316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yandexbuilding',
            name='items',
        ),
        migrations.AddField(
            model_name='buildingitem',
            name='yandex_building',
            field=models.ForeignKey(related_name='items', blank=True, to='estatebase.YandexBuilding', null=True),
        ),
    ]
