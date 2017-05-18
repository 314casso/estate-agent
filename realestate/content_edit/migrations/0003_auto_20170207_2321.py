# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_edit', '0002_auto_20160924_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmscontent',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='cmscontent',
            unique_together=set([('name', 'site')]),
        ),
    ]
