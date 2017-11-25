# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0024_bideventcategory_do_free'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidstate',
            name='event_date',
            field=models.DateTimeField(db_index=True, null=True, verbose_name='Event date', blank=True),
        ),
        migrations.AlterIndexTogether(
            name='bidstate',
            index_together=set([('state', 'event_date')]),
        ),
    ]
