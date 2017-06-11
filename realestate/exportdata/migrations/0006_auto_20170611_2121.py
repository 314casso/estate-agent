# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exportdata', '0005_basefeed_off_queryset_filter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basefeed',
            name='off_queryset_filter',
        ),
        migrations.AddField(
            model_name='basefeed',
            name='min_price_limit',
            field=models.IntegerField(default=100000, verbose_name='MinPriceLimit'),
        ),
        migrations.AddField(
            model_name='basefeed',
            name='only_valid',
            field=models.BooleanField(default=True, verbose_name='OnlyValid'),
        ),
        migrations.AlterField(
            model_name='feedengine',
            name='engine',
            field=models.CharField(default=b'AVITO', max_length=15, choices=[(b'AVITO', b'Avito'), (b'YANDEX', b'Yandex'), (b'WORDPRESS', b'Wordpress')]),
        ),
    ]
