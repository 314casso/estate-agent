# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0035_auto_20210126_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='estate',
            name='estate_number_fake',
            field=models.CharField(max_length=10, null=True, verbose_name='\u041f\u043e\u0434\u0434\u0435\u043b\u044c\u043d\u044b\u0439 \u043d\u043e\u043c\u0435\u0440', blank=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='street_fake',
            field=models.ForeignKey(related_name='fake_streets', on_delete=django.db.models.deletion.PROTECT, verbose_name='\u041f\u043e\u0434\u0434\u0435\u043b\u044c\u043d\u0430\u044f \u0443\u043b\u0438\u0446\u0430', blank=True, to='estatebase.Street', null=True),
        ),
    ]
