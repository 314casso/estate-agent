# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exportdata', '0007_auto_20170611_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='basefeed',
            name='foto_choice',
            field=models.PositiveIntegerField(default=3, verbose_name='EstatePhoto', choices=[(3, '\u0412\u0441\u0435'), (0, '\u041d\u0435\u0442 \u0444\u043e\u0442\u043e'), (1, '\u0415\u0441\u0442\u044c \u0444\u043e\u0442\u043e')]),
        ),
        migrations.AlterField(
            model_name='feedengine',
            name='engine',
            field=models.CharField(default=b'AVITO', max_length=15, choices=[(b'AVITO', b'Avito'), (b'YANDEX', b'Yandex'), (b'WORDPRESS', b'Wordpress'), (b'SITEBILL', b'Sitebill')]),
        ),
    ]
