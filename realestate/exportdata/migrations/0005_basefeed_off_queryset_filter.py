# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exportdata', '0004_auto_20170405_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='basefeed',
            name='off_queryset_filter',
            field=models.BooleanField(default=False, verbose_name='OffQuerysetFilter'),
        ),
    ]
