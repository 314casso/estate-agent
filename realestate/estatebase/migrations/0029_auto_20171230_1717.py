# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0028_estate_actualized'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='estate',
            index_together=set([('id', 'agency_price', 'actualized', 'estate_category')]),
        ),
    ]
