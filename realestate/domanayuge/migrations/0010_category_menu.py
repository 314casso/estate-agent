# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0009_auto_20161001_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='menu',
            field=models.BooleanField(default=True),
        ),
    ]
