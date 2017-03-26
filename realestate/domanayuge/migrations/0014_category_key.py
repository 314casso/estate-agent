# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0013_auto_20170312_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='key',
            field=models.CharField(max_length=50, unique=True, null=True, db_index=True),
        ),
    ]
