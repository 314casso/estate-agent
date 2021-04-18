# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0036_auto_20210128_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='yandexbuilding',
            name='cian_complex_id',
            field=models.CharField(max_length=50, null=True, verbose_name='ID \u0416\u041a \u0432 \u0431\u0430\u0437\u0435 CIAN', blank=True),
        ),
    ]
