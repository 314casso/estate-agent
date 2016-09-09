# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import estatebase.models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0003_auto_20160907_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=estatebase.models.get_profile_upload_to, blank=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid_status',
            field=models.ManyToManyField(to='estatebase.BidStatus', verbose_name='BidStatus', blank=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='brokers',
            field=models.ManyToManyField(to='estatebase.ExUser', verbose_name='User', blank=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='clients',
            field=models.ManyToManyField(related_name='bids_m2m', verbose_name='Clients', to='estatebase.Client', through='estatebase.BidClient', blank=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='estate_categories',
            field=models.ManyToManyField(to='estatebase.EstateTypeCategory', verbose_name='EstateTypeCategory', blank=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='estate_types',
            field=models.ManyToManyField(to='estatebase.EstateType', verbose_name='Estates types', blank=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='estates',
            field=models.ManyToManyField(to='estatebase.Estate', verbose_name='Estate', blank=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='localities',
            field=models.ManyToManyField(to='estatebase.Locality', verbose_name='Locality', blank=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='regions',
            field=models.ManyToManyField(to='estatebase.Region', verbose_name='Regions', blank=True),
        ),
        migrations.AlterField(
            model_name='bidevent',
            name='estates',
            field=models.ManyToManyField(to='estatebase.Estate', verbose_name='Estate', blank=True),
        ),
        migrations.AlterField(
            model_name='bidg',
            name='appliances',
            field=models.ManyToManyField(to='estatebase.Appliance', verbose_name='Appliance', blank=True),
        ),
        migrations.AlterField(
            model_name='bidg',
            name='documents',
            field=models.ManyToManyField(to='estatebase.Document', verbose_name='Documents', blank=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='entrances',
            field=models.ManyToManyField(related_name='estates', verbose_name='Entrances', to='estatebase.Beside', through='estatebase.EntranceEstate', blank=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='estate_params',
            field=models.ManyToManyField(related_name='estates', verbose_name='Estate params', to='estatebase.EstateParam', blank=True),
        ),
        migrations.AlterField(
            model_name='estateregister',
            name='bids',
            field=models.ManyToManyField(related_name='estate_registers', verbose_name='EstateRegisters', to='estatebase.Bid', blank=True),
        ),
        migrations.AlterField(
            model_name='estateregister',
            name='estates',
            field=models.ManyToManyField(related_name='estate_registers', verbose_name='Estate', to='estatebase.Estate', blank=True),
        ),
        migrations.AlterField(
            model_name='stead',
            name='documents',
            field=models.ManyToManyField(to='estatebase.Document', verbose_name='Documents', blank=True),
        ),
    ]
