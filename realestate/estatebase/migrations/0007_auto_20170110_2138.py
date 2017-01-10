# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0006_auto_20161214_2227'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='estate',
            options={'ordering': ['-id'], 'verbose_name': 'estate', 'verbose_name_plural': 'estate', 'permissions': (('view_private', '\u041f\u0440\u043e\u0441\u043c\u043e\u0442\u0440 \u0446\u0435\u043d\u044b, \u043f\u043e\u043b\u043d\u043e\u0433\u043e \u0430\u0434\u0440\u0435\u0441\u0430 \u0438 \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043e\u0432'), ('change_broker', '\u041c\u043e\u0436\u0435\u0442 \u043d\u0430\u0437\u043d\u0430\u0447\u0430\u0442\u044c \u0440\u0438\u044d\u043b\u0442\u043e\u0440\u0430'))},
        ),
        migrations.AlterField(
            model_name='estate',
            name='microdistrict',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Microdistrict', blank=True, to='estatebase.Microdistrict', null=True),
        ),
    ]
