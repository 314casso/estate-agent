# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0034_auto_20180311_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='estate',
            name='latitude',
            field=models.DecimalField(null=True, verbose_name='latitude', max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='longitude',
            field=models.DecimalField(null=True, verbose_name='longitude', max_digits=9, decimal_places=6, blank=True),
        ),
    ]
