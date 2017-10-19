# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0023_auto_20170829_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitemeta',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(size=None, null=True, base_field=models.CharField(max_length=200), blank=True),
        ),
        migrations.AlterField(
            model_name='metatag',
            name='site_meta',
            field=models.ForeignKey(related_name='metatags', to='domanayuge.SiteMeta'),
        ),
    ]
