# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0019_auto_20170924_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='event_date',
            field=models.DateTimeField(null=True, verbose_name='Event date', blank=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='state',
            field=models.PositiveIntegerField(default=1, verbose_name='State', choices=[(1, '\u043d\u043e\u0432\u0430\u044f'), (2, '\u0441\u0432\u043e\u0431\u043e\u0434\u043d\u0430\u044f'), (3, '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), (4, '\u0432 \u043e\u0436\u0438\u0434\u0430\u043d\u0438\u0438'), (5, '\u0437\u0430\u043a\u0440\u044b\u0442\u0430')]),
        ),
        migrations.AlterField(
            model_name='estatefile',
            name='document_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Document type', blank=True, to='estatebase.DocumentType', null=True),
        ),
        migrations.AlterField(
            model_name='estatetype',
            name='name_accs',
            field=models.CharField(max_length=100, null=True, verbose_name='Accs'),
        ),
    ]
