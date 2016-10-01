# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_edit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmscontent',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
