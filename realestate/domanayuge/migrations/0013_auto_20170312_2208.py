# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0012_auto_20170312_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localitydomain',
            name='in_title',
            field=models.BooleanField(default=False, verbose_name='in_title'),
        ),
    ]
