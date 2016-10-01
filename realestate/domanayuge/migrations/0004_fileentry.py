# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import domanayuge.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('domanayuge', '0003_auto_20160926_0004'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(unique=True, verbose_name='Order', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Name', blank=True)),
                ('note', models.CharField(max_length=255, null=True, verbose_name='Note', blank=True)),
                ('file', models.FileField(upload_to=domanayuge.models.get_file_upload_to, verbose_name='File')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
                'verbose_name': 'FileEntriy',
                'verbose_name_plural': 'FileEntries',
            },
        ),
    ]
