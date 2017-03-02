# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0015_auto_20170214_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yandexbuilding',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name', db_index=True),
        ),
        migrations.AlterUniqueTogether(
            name='yandexbuilding',
            unique_together=set([('name', 'locality')]),
        ),
    ]
