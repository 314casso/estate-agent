# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacthistory',
            name='event_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 7, 21, 47, 2, 460584), verbose_name='Event Date'),
        ),
    ]
