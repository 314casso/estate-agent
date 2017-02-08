# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('estatebase', '0013_auto_20170207_2317'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseFeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15, db_index=True)),
                ('active', models.BooleanField()),
                ('valid_days', models.IntegerField()),
                ('note', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentTypeMapper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filter', models.CharField(max_length=255, null=True, blank=True)),
                ('order_by', models.CharField(max_length=150, null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='FeedEngine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15, db_index=True)),
                ('engine', models.CharField(default=b'AVITO', max_length=15, choices=[(b'AVITO', b'Avito'), (b'YANDEX', b'Yandex')])),
            ],
        ),
        migrations.CreateModel(
            name='FeedLocality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed_name', models.CharField(max_length=15, db_index=True)),
                ('feed_code', models.CharField(max_length=15, db_index=True)),
                ('locality', models.ForeignKey(to='estatebase.Locality', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'ordering': ['locality'],
            },
        ),
        migrations.CreateModel(
            name='MappedNode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('xml_node', models.CharField(max_length=50, db_index=True)),
                ('type_mapper', models.ForeignKey(related_name='nodes', to='exportdata.ContentTypeMapper')),
            ],
        ),
        migrations.CreateModel(
            name='MarketingCampaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15, db_index=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('phone', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('person', models.CharField(max_length=255, null=True, blank=True)),
                ('active', models.BooleanField()),
                ('note', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ValueMapper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('xml_value', models.CharField(db_index=True, max_length=255, null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', on_delete=django.db.models.deletion.PROTECT)),
                ('mapped_node', models.ForeignKey(to='exportdata.MappedNode')),
            ],
        ),
        migrations.AddField(
            model_name='contenttypemapper',
            name='feed_engine',
            field=models.ForeignKey(to='exportdata.FeedEngine'),
        ),
        migrations.AddField(
            model_name='basefeed',
            name='campaign',
            field=models.ForeignKey(blank=True, to='exportdata.MarketingCampaign', null=True),
        ),
        migrations.AddField(
            model_name='basefeed',
            name='estate_categories',
            field=models.ManyToManyField(to='estatebase.EstateTypeCategory'),
        ),
        migrations.AddField(
            model_name='basefeed',
            name='estate_param',
            field=models.ForeignKey(blank=True, to='estatebase.EstateParam', null=True),
        ),
        migrations.AddField(
            model_name='basefeed',
            name='estate_types',
            field=models.ManyToManyField(to='estatebase.EstateType', blank=True),
        ),
        migrations.AddField(
            model_name='basefeed',
            name='feed_engine',
            field=models.ForeignKey(to='exportdata.FeedEngine'),
        ),
        migrations.AlterUniqueTogether(
            name='valuemapper',
            unique_together=set([('content_type', 'object_id', 'mapped_node')]),
        ),
        migrations.AlterUniqueTogether(
            name='feedlocality',
            unique_together=set([('feed_code', 'locality')]),
        ),
        migrations.AlterUniqueTogether(
            name='contenttypemapper',
            unique_together=set([('feed_engine', 'content_type')]),
        ),
    ]
