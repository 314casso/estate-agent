# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exportdata', '0002_auto_20170208_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='basefeed',
            name='show_bld_number',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='basefeed',
            name='use_possible_street',
            field=models.BooleanField(default=False),
        ),
    ]
