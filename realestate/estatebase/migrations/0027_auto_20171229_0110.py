# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0026_auto_20171125_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='updated',
            field=models.DateTimeField(db_index=True, null=True, verbose_name='Updated', blank=True),
        ),
    ]
