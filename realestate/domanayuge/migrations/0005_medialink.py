# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import domanayuge.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('domanayuge', '0004_fileentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(unique=True, verbose_name='Order', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('url', models.URLField(max_length=100, null=True, verbose_name='url', blank=True)),
                ('icon_class', models.CharField(max_length=50, verbose_name='Icon class')),
                ('image', models.ImageField(upload_to=domanayuge.models.get_file_upload_to, verbose_name='Image')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
                'verbose_name': 'MediaLink',
                'verbose_name_plural': 'MediaLinks',
            },
        ),
    ]
