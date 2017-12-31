# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0027_auto_20171229_0110'),
    ]

    operations = [
        migrations.AddField(
            model_name='estate',
            name='actualized',
            field=models.DateTimeField(default=datetime.date(2000, 1, 1), verbose_name='Modificated', db_index=True),
        ),
    ]
