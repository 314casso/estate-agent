# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0019_contententry_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='alternate_title',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
    ]
