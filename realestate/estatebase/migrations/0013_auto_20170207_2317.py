# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0012_auto_20170202_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingitem',
            name='total_area_max',
            field=models.DecimalField(null=True, verbose_name='Total area max', max_digits=10, decimal_places=2, blank=True),
        ),
    ]
