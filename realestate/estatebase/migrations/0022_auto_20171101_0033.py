# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0021_auto_20171101_0004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bid_state',
        ),
        migrations.AddField(
            model_name='bidstate',
            name='bid',
            field=models.OneToOneField(related_name='state', default=1, verbose_name='Bid', to='estatebase.Bid'),
            preserve_default=False,
        ),
    ]
