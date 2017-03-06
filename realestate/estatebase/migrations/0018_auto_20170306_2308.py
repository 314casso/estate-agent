# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0017_auto_20170302_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingitem',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name', db_index=True),
        ),
        migrations.AlterField(
            model_name='yandexbuilding',
            name='building_id',
            field=models.CharField(db_index=True, max_length=50, null=True, verbose_name='Yandex building id', blank=True),
        ),
    ]
