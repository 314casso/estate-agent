# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0016_auto_20170302_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estate',
            name='beside',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Beside', blank=True, to='estatebase.Beside', null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='broker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Broker', blank=True, to='estatebase.ExUser', null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Contact', blank=True, to='estatebase.Contact', null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='deal_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='DealStatus', blank=True, to='estatebase.DealStatus', null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='driveway',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Driveway', blank=True, to='estatebase.Driveway', null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='electricity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Electricity', blank=True, to='estatebase.Electricity', null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='gassupply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Gassupply', blank=True, to='estatebase.Gassupply', null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='history',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='estatebase.HistoryMeta'),
        ),
        migrations.AlterField(
            model_name='estate',
            name='internet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Internet', blank=True, to='estatebase.Internet', null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Origin', blank=True, to='estatebase.Origin', null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='sewerage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Sewerage', blank=True, to='estatebase.Sewerage', null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='telephony',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Telephony', blank=True, to='estatebase.Telephony', null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='validity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Validity', blank=True, to='estatebase.Validity', null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='watersupply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Watersupply', blank=True, to='estatebase.Watersupply', null=True),
        ),
    ]
