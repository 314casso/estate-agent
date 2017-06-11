# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exportdata', '0003_auto_20170215_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basefeed',
            name='active',
            field=models.BooleanField(verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='campaign',
            field=models.ForeignKey(verbose_name='Campaign', blank=True, to='exportdata.MarketingCampaign', null=True),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='estate_categories',
            field=models.ManyToManyField(to='estatebase.EstateTypeCategory', verbose_name='EstateTypeCategory'),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='estate_param',
            field=models.ForeignKey(verbose_name='EstateParam', blank=True, to='estatebase.EstateParam', null=True),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='estate_types',
            field=models.ManyToManyField(to='estatebase.EstateType', verbose_name='EstateType', blank=True),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='feed_engine',
            field=models.ForeignKey(verbose_name='FeedEngine', to='exportdata.FeedEngine'),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='name',
            field=models.CharField(max_length=15, verbose_name='Name', db_index=True),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='note',
            field=models.CharField(max_length=255, null=True, verbose_name='Note', blank=True),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='show_bld_number',
            field=models.BooleanField(default=False, verbose_name='ShowBldNumber'),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='use_broker',
            field=models.BooleanField(default=False, verbose_name='UseBroker'),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='use_possible_street',
            field=models.BooleanField(default=False, verbose_name='UsePossibleStreet'),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='valid_days',
            field=models.IntegerField(verbose_name='ValidDays'),
        ),
    ]
