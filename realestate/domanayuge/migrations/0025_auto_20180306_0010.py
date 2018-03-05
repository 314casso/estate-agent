# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0024_auto_20171019_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contententry',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug'),
        ),
    ]
