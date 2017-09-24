# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0018_auto_20170306_2308'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Document type',
                'verbose_name_plural': 'Document types',
            },
        ),
        migrations.AddField(
            model_name='estatefile',
            name='document_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='estatebase.DocumentType', null=True),
        ),
    ]
