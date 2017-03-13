# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0011_localitydomain'),
    ]

    operations = [
        migrations.AddField(
            model_name='localitydomain',
            name='active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AddField(
            model_name='localitydomain',
            name='in_title',
            field=models.BooleanField(default=True, verbose_name='in_title'),
        ),
    ]
