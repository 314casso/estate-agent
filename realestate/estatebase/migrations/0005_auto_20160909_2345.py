# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import estatebase.models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0004_auto_20160909_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=estatebase.models.get_profile_upload_to, null=True, verbose_name='File', blank=True),
        ),
    ]
