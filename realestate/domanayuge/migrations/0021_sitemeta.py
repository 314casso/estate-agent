# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('domanayuge', '0020_auto_20170522_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('main_mirror', models.CharField(max_length=150, null=True, blank=True)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
        ),
    ]
