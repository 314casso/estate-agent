# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0022_auto_20171101_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='bideventcategory',
            name='is_calendar',
            field=models.BooleanField(default=False, verbose_name='Calendar'),
        ),
    ]
