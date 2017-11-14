# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0020_auto_20171019_2158'),
    ]

    operations = [
        migrations.CreateModel(
            name='BidState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.PositiveIntegerField(default=1, verbose_name='State', choices=[(1, '\u043d\u043e\u0432\u0430\u044f'), (2, '\u0441\u0432\u043e\u0431\u043e\u0434\u043d\u0430\u044f'), (3, '\u0432 \u0440\u0430\u0431\u043e\u0442\u0435'), (4, '\u0432 \u043e\u0436\u0438\u0434\u0430\u043d\u0438\u0438'), (5, '\u0437\u0430\u043a\u0440\u044b\u0442\u0430')])),
                ('event_date', models.DateTimeField(null=True, verbose_name='Event date', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='bid',
            name='event_date',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='state',
        ),
        migrations.AddField(
            model_name='bid',
            name='bid_state',
            field=models.OneToOneField(null=True, blank=True, editable=False, to='estatebase.BidState'),
        ),
    ]
