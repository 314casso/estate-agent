# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0025_auto_20171125_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidstate',
            name='state',
            field=models.PositiveIntegerField(default=1, db_index=True, verbose_name='State', choices=[(1, '\u043d\u043e\u0432\u0430\u044f'), (2, '\u0441\u0432\u043e\u0431\u043e\u0434\u043d\u0430\u044f'), (3, '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), (4, '\u0432 \u043e\u0436\u0438\u0434\u0430\u043d\u0438\u0438'), (5, '\u0437\u0430\u043a\u0440\u044b\u0442\u0430')]),
        ),
    ]
