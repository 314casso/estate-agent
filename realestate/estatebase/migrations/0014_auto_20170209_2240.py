# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0013_auto_20170207_2317'),
    ]

    operations = [
        migrations.CreateModel(
            name='BidStatusCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Bid status category',
                'verbose_name_plural': 'Bid status categories',
            },
        ),
        migrations.AddField(
            model_name='bidstatus',
            name='category',
            field=models.ForeignKey(related_name='statuses', verbose_name='Category', blank=True, to='estatebase.BidStatusCategory', null=True),
        ),
    ]
