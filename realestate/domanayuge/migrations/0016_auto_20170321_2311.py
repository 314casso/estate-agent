# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0015_auto_20170321_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='key',
            field=models.CharField(unique=True, max_length=50, db_index=True),
        ),
    ]
