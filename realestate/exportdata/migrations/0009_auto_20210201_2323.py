# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exportdata', '0008_auto_20200608_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basefeed',
            name='estate_categories',
            field=models.ManyToManyField(help_text='\u0423\u043a\u0430\u0437\u044b\u0432\u0430\u0439\u0442\u0435 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044e \u0442\u043e\u043b\u044c\u043a\u043e \u0432 \u0442\u043e\u043c \u0441\u043b\u0443\u0447\u0430\u0435, \u0435\u0441\u043b\u0438 \u043d\u0443\u0436\u043d\u043e \u043e\u0442\u043e\u0431\u0440\u0430\u0442\u044c \u0435\u0435 \u043f\u043e\u043b\u043d\u043e\u0441\u0442\u044c\u044e, \u0431\u0435\u0437 \u0440\u0430\u0437\u0431\u0438\u0432\u043a\u0438 \u043f\u043e \u0432\u0438\u0434\u0430\u043c.', to='estatebase.EstateTypeCategory', verbose_name='EstateTypeCategory'),
        ),
        migrations.AlterField(
            model_name='basefeed',
            name='estate_types',
            field=models.ManyToManyField(help_text='\u0415\u0441\u043b\u0438 \u0432\u0438\u0434 \u043d\u0435\u0434\u0432\u0438\u0436\u0438\u043c\u043e\u0441\u0442\u0438 \u0443\u043a\u0430\u0437\u0430\u043d, \u0442\u043e \u0435\u0433\u043e \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f, \u0434\u0430\u0436\u0435 \u0435\u0441\u043b\u0438 \u043e\u043d\u0430 \u0432\u044b\u0431\u0440\u0430\u043d\u0430 \u0440\u0430\u043d\u0435\u0435, \u043d\u0435 \u0431\u0443\u0434\u0435\u0442 \u0443\u0447\u0438\u0442\u044b\u0432\u0430\u0442\u044c\u0441\u044f \u0432 \u043e\u0442\u0431\u043e\u0440\u0435.', to='estatebase.EstateType', verbose_name='EstateType', blank=True),
        ),
    ]
