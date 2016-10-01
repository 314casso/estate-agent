# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0007_auto_20160928_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileentry',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='FileEntry',
        ),
    ]
