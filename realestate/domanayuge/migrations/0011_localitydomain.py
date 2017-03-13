# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0018_auto_20170306_2308'),
        ('domanayuge', '0010_category_menu'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalityDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(db_index=True, max_length=150, blank=True)),
                ('locality', models.ForeignKey(to='estatebase.Locality')),
            ],
        ),
    ]
