# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0033_auto_20180204_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='locality',
            name='latitude',
            field=models.DecimalField(null=True, verbose_name='latitude', max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AddField(
            model_name='locality',
            name='longitude',
            field=models.DecimalField(null=True, verbose_name='longitude', max_digits=9, decimal_places=6, blank=True),
        ),
    ]
