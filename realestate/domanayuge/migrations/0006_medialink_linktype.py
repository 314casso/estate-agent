# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0005_medialink'),
    ]

    operations = [
        migrations.AddField(
            model_name='medialink',
            name='linktype',
            field=models.PositiveIntegerField(default=1, verbose_name='Type', choices=[(1, '\u0421\u0441\u044b\u043b\u043a\u0430'), (2, '\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0430'), (3, '\u041a\u043e\u043d\u0442\u0430\u043a\u0442'), (4, '\u041c\u0435\u0441\u0441\u0435\u043d\u0434\u0436\u0435\u0440'), (5, '\u0421\u043e\u0446\u0441\u0435\u0442\u044c')]),
        ),
    ]
