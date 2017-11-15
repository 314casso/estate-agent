# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0023_bideventcategory_is_calendar'),
    ]

    operations = [
        migrations.AddField(
            model_name='bideventcategory',
            name='do_free',
            field=models.BooleanField(default=False, verbose_name='Free'),
        ),
    ]
