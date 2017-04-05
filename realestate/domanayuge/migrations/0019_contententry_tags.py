# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0018_auto_20170326_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='contententry',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(size=None, null=True, base_field=models.CharField(max_length=200), blank=True),
        ),
    ]
