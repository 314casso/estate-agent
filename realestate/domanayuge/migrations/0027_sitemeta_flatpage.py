# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0026_auto_20180516_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitemeta',
            name='flatpage',
            field=models.TextField(null=True, blank=True),
        ),
    ]
