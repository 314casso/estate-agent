# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0027_sitemeta_flatpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitemeta',
            name='after_body',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sitemeta',
            name='after_head',
            field=models.TextField(null=True, blank=True),
        ),
    ]
