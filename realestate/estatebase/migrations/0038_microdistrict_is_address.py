# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0037_yandexbuilding_cian_complex_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='microdistrict',
            name='is_address',
            field=models.BooleanField(default=False, verbose_name='\u0412\u043a\u043b\u044e\u0447\u0430\u0442\u044c \u0432 \u0430\u0434\u0440\u0435\u0441'),
        ),
    ]
