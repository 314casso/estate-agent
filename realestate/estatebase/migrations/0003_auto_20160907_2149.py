# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0002_auto_20160907_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacthistory',
            name='event_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Event Date'),
        ),
    ]
