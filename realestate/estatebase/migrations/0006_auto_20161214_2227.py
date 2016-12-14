# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0005_auto_20160909_2345'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['-history__created'], 'verbose_name': 'Bid', 'verbose_name_plural': 'Bids', 'permissions': (('view_other_bid', '\u041f\u0440\u043e\u0441\u043c\u043e\u0442\u0440 \u0447\u0443\u0436\u0438\u0445 \u0437\u0430\u044f\u0432\u043e\u043a'),)},
        ),
    ]
