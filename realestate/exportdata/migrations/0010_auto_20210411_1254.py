# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exportdata', '0009_auto_20210201_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedengine',
            name='engine',
            field=models.CharField(default=b'AVITO', max_length=15, choices=[(b'AVITO', b'Avito'), (b'YANDEX', b'Yandex'), (b'WORDPRESS', b'Wordpress'), (b'SITEBILL', b'Sitebill'), (b'CIAN', b'Cian')]),
        ),
    ]
