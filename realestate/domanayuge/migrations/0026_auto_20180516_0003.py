# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0025_auto_20180306_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='contententry',
            name='meta_description',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contententry',
            name='meta_title',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
