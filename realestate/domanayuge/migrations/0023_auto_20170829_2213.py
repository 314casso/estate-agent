# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0022_auto_20170829_0022'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, null=True, blank=True)),
                ('content', models.CharField(max_length=250, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='sitemeta',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sitemeta',
            name='keywords',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sitemeta',
            name='title',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='metatag',
            name='site_meta',
            field=models.ForeignKey(to='domanayuge.SiteMeta'),
        ),
    ]
