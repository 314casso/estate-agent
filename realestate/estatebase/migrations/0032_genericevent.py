# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('estatebase', '0031_create_custom_estate_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('date', models.DateTimeField(null=True, verbose_name='Event date', blank=True)),
                ('note', models.TextField(null=True, verbose_name='Note', blank=True)),
                ('category', models.ForeignKey(verbose_name='Category', to='estatebase.BidEventCategory')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('history', models.OneToOneField(null=True, blank=True, editable=False, to='estatebase.HistoryMeta')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'bid event',
                'verbose_name_plural': 'bid events',
            },
        ),
    ]
