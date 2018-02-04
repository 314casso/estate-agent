# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0032_genericevent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genericevent',
            options={'ordering': ['-date'], 'verbose_name': 'event', 'verbose_name_plural': 'events'},
        ),
        migrations.AddField(
            model_name='genericevent',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]
