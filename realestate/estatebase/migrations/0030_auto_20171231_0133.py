# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0029_auto_20171230_1717'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='estate',
            unique_together=set([('id', 'agency_price', 'actualized', 'estate_category')]),
        ),
        migrations.AlterIndexTogether(
            name='estate',
            index_together=set([]),
        ),
    ]
