# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import domanayuge.models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0017_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to=domanayuge.models.get_file_upload_to, null=True, verbose_name='Image', blank=True),
        ),
    ]
