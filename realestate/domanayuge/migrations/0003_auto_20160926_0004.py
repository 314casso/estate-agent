# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0002_category_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now, help_text="Used to build the entry's URL.", verbose_name='publication date', db_index=True)),
                ('summary', models.TextField(null=True, verbose_name='summary', blank=True)),
                ('content', models.TextField(verbose_name='content', blank=True)),
                ('categories', models.ManyToManyField(related_name='entries', to='domanayuge.Category')),
            ],
            options={
                'ordering': ['-publication_date'],
                'get_latest_by': 'publication_date',
                'verbose_name': 'entry',
                'verbose_name_plural': 'entries',
            },
        ),
        migrations.AlterIndexTogether(
            name='contententry',
            index_together=set([('slug', 'publication_date')]),
        ),
    ]
