# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exportdata', '0006_auto_20170611_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basefeed',
            name='min_price_limit',
            field=models.IntegerField(default=100000, null=True, verbose_name='MinPriceLimit', blank=True),
        ),
    ]
