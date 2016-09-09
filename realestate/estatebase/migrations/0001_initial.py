# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import datetime
import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
import estatebase.models
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_auto_20160907_2122'),
        ('devrep', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appliance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Appliance',
                'verbose_name_plural': 'Appliances',
            },
        ),
        migrations.CreateModel(
            name='Beside',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
                ('name_gent', models.CharField(max_length=255, null=True, verbose_name='Gent', blank=True)),
                ('name_loct', models.CharField(max_length=255, null=True, verbose_name='Loct', blank=True)),
                ('name_dativ', models.CharField(max_length=255, null=True, verbose_name='Dativ', blank=True)),
                ('name_accus', models.CharField(max_length=255, null=True, verbose_name='Accus', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'beside',
                'verbose_name_plural': 'besides',
            },
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('estate_filter', picklefield.fields.PickledObjectField(null=True, editable=False, blank=True)),
                ('cleaned_filter', picklefield.fields.PickledObjectField(null=True, editable=False, blank=True)),
                ('agency_price_min', models.IntegerField(null=True, verbose_name='Price min', blank=True)),
                ('agency_price_max', models.IntegerField(null=True, verbose_name='Price max', blank=True)),
                ('note', models.TextField(null=True, verbose_name='Note', blank=True)),
            ],
            options={
                'ordering': ['-history__created'],
                'verbose_name': 'Bid',
                'verbose_name_plural': 'Bids',
            },
        ),
        migrations.CreateModel(
            name='BidClient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bid', models.ForeignKey(to='estatebase.Bid')),
            ],
        ),
        migrations.CreateModel(
            name='BidEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(null=True, verbose_name='Event date', blank=True)),
                ('note', models.TextField(null=True, verbose_name='Note', blank=True)),
                ('bid', models.ForeignKey(related_name='bid_events', verbose_name='Bid', to='estatebase.Bid')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'bid event',
                'verbose_name_plural': 'bid events',
            },
        ),
        migrations.CreateModel(
            name='BidEventCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'BidEventCategory',
                'verbose_name_plural': 'BidEventCategories',
            },
        ),
        migrations.CreateModel(
            name='Bidg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room_number', models.CharField(max_length=10, null=True, verbose_name='Room number', blank=True)),
                ('year_built', models.PositiveIntegerField(blank=True, null=True, verbose_name='Year built', validators=[estatebase.models.validate_year])),
                ('floor', models.PositiveIntegerField(null=True, verbose_name='Floor', blank=True)),
                ('floor_count', models.DecimalField(null=True, verbose_name='Floor count', max_digits=3, decimal_places=1, blank=True)),
                ('elevator', models.BooleanField(default=False, verbose_name='Elevator')),
                ('ceiling_height', models.DecimalField(null=True, verbose_name='Ceiling height', max_digits=5, decimal_places=2, blank=True)),
                ('room_count', models.PositiveIntegerField(null=True, verbose_name='Room count', blank=True)),
                ('total_area', models.DecimalField(null=True, verbose_name='Total area', max_digits=10, decimal_places=2, blank=True)),
                ('used_area', models.DecimalField(null=True, verbose_name='Used area', max_digits=10, decimal_places=2, blank=True)),
                ('basic', models.BooleanField(default=False, verbose_name='Basic')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('appliances', models.ManyToManyField(to='estatebase.Appliance', null=True, verbose_name='Appliance', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'bidg',
                'verbose_name_plural': 'bidgs',
            },
        ),
        migrations.CreateModel(
            name='BidStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Bid status',
                'verbose_name_plural': 'Bid statuss',
            },
        ),
        migrations.CreateModel(
            name='Ceiling',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Ceiling',
                'verbose_name_plural': 'Ceilings',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='Address', blank=True)),
                ('note', models.TextField(null=True, verbose_name='Note', blank=True)),
                ('has_dev_profile', models.BooleanField(default=False, verbose_name='HasDevProfile')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
            },
        ),
        migrations.CreateModel(
            name='ClientType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'client type',
                'verbose_name_plural': 'client types',
            },
        ),
        migrations.CreateModel(
            name='ComStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
                ('status', models.IntegerField(verbose_name='Status', choices=[(1, '\u0414\u0430'), (0, '\u041d\u0435\u0442'), (2, '\u0412\u043e\u0437\u043c\u043e\u0436\u043d\u043e')])),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Com status',
                'verbose_name_plural': 'Com statuses',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact', models.CharField(unique=True, max_length=255, verbose_name='Contact', db_index=True)),
                ('updated', models.DateTimeField(null=True, verbose_name='Updated', blank=True)),
                ('client', models.ForeignKey(related_name='contacts', verbose_name='Client', to='estatebase.Client')),
            ],
            options={
                'ordering': ['contact_state__id', 'contact_type__id'],
                'verbose_name': 'contact',
                'verbose_name_plural': 'contacts',
            },
        ),
        migrations.CreateModel(
            name='ContactHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_date', models.DateTimeField(default=datetime.datetime(2016, 9, 7, 21, 46, 34, 922107), verbose_name='Event Date')),
                ('contact', models.ForeignKey(verbose_name='Contact', to='estatebase.Contact')),
            ],
            options={
                'verbose_name': 'contact history',
                'verbose_name_plural': 'contact history',
            },
        ),
        migrations.CreateModel(
            name='ContactState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'contact state',
                'verbose_name_plural': 'contact states',
            },
        ),
        migrations.CreateModel(
            name='ContactType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'contact type',
                'verbose_name_plural': 'contact types',
            },
        ),
        migrations.CreateModel(
            name='DealStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'DealStatus',
                'verbose_name_plural': 'DealStatuses',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
            },
        ),
        migrations.CreateModel(
            name='Driveway',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'driveway',
                'verbose_name_plural': 'driveways',
            },
        ),
        migrations.CreateModel(
            name='Electricity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'electricity',
                'verbose_name_plural': 'electricities',
            },
        ),
        migrations.CreateModel(
            name='EntranceEstate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(verbose_name='Type', choices=[(1, '\u0412\u044b\u0445\u043e\u0434'), (2, '\u0412\u0438\u0434'), (3, '\u0420\u0430\u0441\u0441\u0442\u043e\u044f\u043d\u0438\u0435'), (4, '\u0412\u0438\u0434 \u0438\u0437 \u043e\u043a\u043d\u0430')])),
                ('distance', models.IntegerField(null=True, verbose_name='Distance', blank=True)),
                ('basic', models.BooleanField(default=False, verbose_name='Basic')),
                ('beside', models.ForeignKey(verbose_name='Object', to='estatebase.Beside')),
            ],
        ),
        migrations.CreateModel(
            name='Estate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('address_state', models.PositiveIntegerField(blank=True, null=True, verbose_name='Address state', choices=[(1, '\u041d\u0435\u0442 \u0443\u043b\u0438\u0446\u044b'), (2, '\u041d\u0435\u0442 \u043d\u043e\u043c\u0435\u0440\u0430'), (3, '\u041d\u0435\u0442 \u0430\u0434\u0440\u0435\u0441\u0430')])),
                ('estate_number', models.CharField(max_length=10, null=True, verbose_name='Estate number', blank=True)),
                ('beside_distance', models.PositiveIntegerField(null=True, verbose_name='Beside distance', blank=True)),
                ('saler_price', models.PositiveIntegerField(null=True, verbose_name='Saler price', blank=True)),
                ('agency_price', models.PositiveIntegerField(null=True, verbose_name='Agency price', blank=True)),
                ('electricity_distance', models.PositiveIntegerField(null=True, verbose_name=b'Electricity distance', blank=True)),
                ('watersupply_distance', models.PositiveIntegerField(null=True, verbose_name='Watersupply distance', blank=True)),
                ('gassupply_distance', models.PositiveIntegerField(null=True, verbose_name='Gassupply distance', blank=True)),
                ('sewerage_distance', models.PositiveIntegerField(null=True, verbose_name='Sewerage distance', blank=True)),
                ('driveway_distance', models.PositiveIntegerField(null=True, verbose_name='Driveway distance', blank=True)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('client_description', models.TextField(null=True, verbose_name='Client description', blank=True)),
                ('comment', models.TextField(max_length=255, null=True, verbose_name='Comment', blank=True)),
                ('beside', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Beside', blank=True, to='estatebase.Beside', null=True)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'estate',
                'verbose_name_plural': 'estate',
                'permissions': (('view_private', '\u041f\u0440\u043e\u0441\u043c\u043e\u0442\u0440 \u0446\u0435\u043d\u044b, \u043f\u043e\u043b\u043d\u043e\u0433\u043e \u0430\u0434\u0440\u0435\u0441\u0430 \u0438 \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043e\u0432'),),
            },
        ),
        migrations.CreateModel(
            name='EstateClient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client', models.ForeignKey(to='estatebase.Client')),
                ('estate', models.ForeignKey(to='estatebase.Estate')),
            ],
        ),
        migrations.CreateModel(
            name='EstateClientStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Estate client status',
                'verbose_name_plural': 'Estate client statuss',
            },
        ),
        migrations.CreateModel(
            name='EstateFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(unique=True, verbose_name='Order', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Name', blank=True)),
                ('note', models.CharField(max_length=255, null=True, verbose_name='Note', blank=True)),
                ('file', models.FileField(upload_to=estatebase.models.get_file_upload_to, verbose_name='File')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
                'verbose_name': 'EstateFile',
                'verbose_name_plural': 'EstateFiles',
            },
        ),
        migrations.CreateModel(
            name='EstateParam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(unique=True, verbose_name='Order', blank=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
                'verbose_name': 'estate param',
                'verbose_name_plural': 'estate params',
            },
        ),
        migrations.CreateModel(
            name='EstatePhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(unique=True, verbose_name='Order', blank=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Name', blank=True)),
                ('note', models.CharField(max_length=255, null=True, verbose_name='Note', blank=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=estatebase.models.get_upload_to)),
                ('estate', models.ForeignKey(related_name='images', verbose_name='Estate', to='estatebase.Estate')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
                'verbose_name': 'EstatePhoto',
                'verbose_name_plural': 'EstatePhotos',
            },
        ),
        migrations.CreateModel(
            name='EstateRegister',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('bids', models.ManyToManyField(related_name='estate_registers', null=True, verbose_name='EstateRegisters', to='estatebase.Bid', blank=True)),
                ('estates', models.ManyToManyField(related_name='estate_registers', null=True, verbose_name='Estate', to='estatebase.Estate', blank=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EstateStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'estate status',
                'verbose_name_plural': 'estate statuses',
            },
        ),
        migrations.CreateModel(
            name='EstateType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(unique=True, verbose_name='Order', blank=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('name_accs', models.CharField(max_length=100, null=True, verbose_name='Accs', blank=True)),
                ('template', models.IntegerField(verbose_name='Template', choices=[(0, '\u041a\u0432\u0430\u0440\u0442\u0438\u0440\u0430'), (1, '\u041d\u043e\u0432\u043e\u0441\u0442\u0440\u043e\u0439\u043a\u0430'), (2, '\u0414\u043e\u043c'), (3, '\u0423\u0447\u0430\u0441\u0442\u043e\u043a'), (4, '\u041f\u043e\u0441\u0442\u0440\u043e\u0439\u043a\u0430'), (5, '\u0421\u0435\u043b\u044c\u0445\u043e\u0437. \u0443\u0447\u0430\u0441\u0442\u043e\u043a'), (6, '\u041a\u0432\u0430\u0440\u0442\u0438\u0440\u0430 \u0441 \u0443\u0447\u0430\u0441\u0442\u043a\u043e\u043c'), (7, '\u0421\u043e\u043e\u0440\u0443\u0436\u0435\u043d\u0438\u0435'), (8, '\u0411\u043b\u0430\u0433\u043e\u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u043e'), (9, '\u0413\u0430\u0440\u0430\u0436')])),
                ('note', models.CharField(max_length=255, null=True, verbose_name='Note', blank=True)),
                ('placeable', models.BooleanField(default=True, verbose_name='Placeable')),
            ],
            options={
                'ordering': ['estate_type_category__order', 'name'],
                'abstract': False,
                'verbose_name': 'estate type',
                'verbose_name_plural': 'estate types',
            },
        ),
        migrations.CreateModel(
            name='EstateTypeCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(unique=True, verbose_name='Order', blank=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('independent', models.BooleanField(default=True, verbose_name='Independent')),
                ('has_bidg', models.IntegerField(verbose_name='HasBidg', choices=[(1, '\u0414\u0430'), (0, '\u041d\u0435\u0442'), (2, '\u0412\u043e\u0437\u043c\u043e\u0436\u043d\u043e')])),
                ('has_stead', models.IntegerField(verbose_name='HasStead', choices=[(1, '\u0414\u0430'), (0, '\u041d\u0435\u0442'), (2, '\u0412\u043e\u0437\u043c\u043e\u0436\u043d\u043e')])),
                ('is_commerce', models.BooleanField(default=False, verbose_name='Commerce')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
                'verbose_name': 'estate type category',
                'verbose_name_plural': 'estate type categories',
            },
        ),
        migrations.CreateModel(
            name='ExteriorFinish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'exterior finish',
                'verbose_name_plural': 'exterior finishs',
            },
        ),
        migrations.CreateModel(
            name='Flooring',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Flooring',
                'verbose_name_plural': 'Floorings',
            },
        ),
        migrations.CreateModel(
            name='Furniture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Furniture',
                'verbose_name_plural': 'Furnitures',
            },
        ),
        migrations.CreateModel(
            name='Gassupply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'gassupply',
                'verbose_name_plural': 'gassupplies',
            },
        ),
        migrations.CreateModel(
            name='GenericLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Name', blank=True)),
                ('url', models.CharField(max_length=100, null=True, verbose_name='Url', blank=True)),
                ('note', models.CharField(max_length=255, null=True, verbose_name='Note', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'GenericLink',
                'verbose_name_plural': 'GenericLinks',
            },
        ),
        migrations.CreateModel(
            name='GeoGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Geo group',
                'verbose_name_plural': 'Geo groups',
            },
        ),
        migrations.CreateModel(
            name='Heating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'heating',
                'verbose_name_plural': 'heatings',
            },
        ),
        migrations.CreateModel(
            name='HistoryMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='Created', db_index=True)),
                ('updated', models.DateTimeField(db_index=True, null=True, verbose_name='Updated', blank=True)),
                ('modificated', models.DateTimeField(verbose_name='Modificated', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Interior',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Interior',
                'verbose_name_plural': 'Interiors',
            },
        ),
        migrations.CreateModel(
            name='Internet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'internet',
                'verbose_name_plural': 'internets',
            },
        ),
        migrations.CreateModel(
            name='LandType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Land type',
                'verbose_name_plural': 'Land types',
            },
        ),
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.DecimalField(null=True, verbose_name='Area', max_digits=7, decimal_places=2, blank=True)),
                ('note', models.CharField(max_length=255, null=True, verbose_name='Note', blank=True)),
                ('furniture', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Furniture', blank=True, to='estatebase.Furniture', null=True)),
                ('interior', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Interior', blank=True, to='estatebase.Interior', null=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'layout',
                'verbose_name_plural': 'layouts',
            },
        ),
        migrations.CreateModel(
            name='LayoutFeature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Layout feature',
                'verbose_name_plural': 'Layout features',
            },
        ),
        migrations.CreateModel(
            name='LayoutType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
                ('layout_category', models.IntegerField(blank=True, null=True, verbose_name='Category', choices=[(1, '\u0416\u0438\u043b\u0430\u044f \u043f\u043b\u043e\u0449\u0430\u0434\u044c'), (2, '\u041a\u0443\u0445\u043d\u044f')])),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Layout type',
                'verbose_name_plural': 'Layout types',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bidg', models.ForeignKey(related_name='levels', verbose_name='Level', to='estatebase.Bidg')),
            ],
            options={
                'ordering': ['level_name'],
                'verbose_name': 'Level',
                'verbose_name_plural': 'Levels',
            },
        ),
        migrations.CreateModel(
            name='LevelName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Level name',
                'verbose_name_plural': 'Level names',
            },
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('name_gent', models.CharField(max_length=255, null=True, verbose_name='Gent', blank=True)),
                ('name_loct', models.CharField(max_length=255, null=True, verbose_name='Loct', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'locality',
                'verbose_name_plural': 'localities',
            },
        ),
        migrations.CreateModel(
            name='LocalityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
                ('sort_name', models.CharField(max_length=50, verbose_name='Short name', db_index=True)),
                ('prep_name', models.CharField(max_length=255, verbose_name='Prepositional Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'LocalityType',
                'verbose_name_plural': 'LocalityTypes',
            },
        ),
        migrations.CreateModel(
            name='Microdistrict',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('locality', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Locality', to='estatebase.Locality')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'microdistrict',
                'verbose_name_plural': 'microdistricts',
            },
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
                ('address', models.TextField(verbose_name='Address')),
                ('address_short', models.TextField(verbose_name='Short address')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Office',
                'verbose_name_plural': 'Offices',
            },
        ),
        migrations.CreateModel(
            name='Origin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'origin',
                'verbose_name_plural': 'origins',
            },
        ),
        migrations.CreateModel(
            name='Purpose',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Purpose',
                'verbose_name_plural': 'Purposes',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
                ('regular_name', models.CharField(max_length=100, null=True, verbose_name='Region', blank=True)),
                ('regular_name_gent', models.CharField(max_length=100, null=True, verbose_name='Gent', blank=True)),
                ('geo_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='GeoGroup', to='estatebase.GeoGroup')),
                ('metropolis', models.ForeignKey(related_name='metropolis_region', on_delete=django.db.models.deletion.PROTECT, verbose_name='\u0420\u0430\u0439\u0446\u0435\u043d\u0442\u0440', blank=True, to='estatebase.Locality', null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'region',
                'verbose_name_plural': 'regions',
            },
        ),
        migrations.CreateModel(
            name='RegisterCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Register category',
                'verbose_name_plural': 'Register categorys',
            },
        ),
        migrations.CreateModel(
            name='Roof',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Roof',
                'verbose_name_plural': 'Roofs',
            },
        ),
        migrations.CreateModel(
            name='Sewerage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'sewerage',
                'verbose_name_plural': 'sewerages',
            },
        ),
        migrations.CreateModel(
            name='Shape',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Shape',
                'verbose_name_plural': 'Shapes',
            },
        ),
        migrations.CreateModel(
            name='Stead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_area', models.DecimalField(null=True, verbose_name='Total area', max_digits=10, decimal_places=2, blank=True)),
                ('face_area', models.DecimalField(null=True, verbose_name='Face area', max_digits=10, decimal_places=2, blank=True)),
                ('cadastral_number', models.CharField(max_length=150, null=True, verbose_name='Cadastral number', blank=True)),
                ('documents', models.ManyToManyField(to='estatebase.Document', null=True, verbose_name='Documents', blank=True)),
                ('estate', models.OneToOneField(related_name='stead', verbose_name='Estate', to='estatebase.Estate')),
                ('estate_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=15, verbose_name='EstateType', to='estatebase.EstateType')),
                ('land_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='LandType', blank=True, to='estatebase.LandType', null=True)),
                ('purpose', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Purpose', blank=True, to='estatebase.Purpose', null=True)),
                ('shape', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Shape', blank=True, to='estatebase.Shape', null=True)),
            ],
            options={
                'verbose_name': 'stead',
                'verbose_name_plural': 'steads',
            },
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('locality', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Locality', to='estatebase.Locality')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'street',
                'verbose_name_plural': 'streets',
            },
        ),
        migrations.CreateModel(
            name='StreetType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
                ('sort_name', models.CharField(max_length=50, verbose_name='Short name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'StreetType',
                'verbose_name_plural': 'StreetTypes',
            },
        ),
        migrations.CreateModel(
            name='Telephony',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'telephony',
                'verbose_name_plural': 'telephonies',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=255, null=True, verbose_name='Phone', blank=True)),
                ('geo_groups', models.ManyToManyField(to='estatebase.GeoGroup', verbose_name='Geo group')),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Office', blank=True, to='estatebase.Office', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Validity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Validity',
                'verbose_name_plural': 'Validitys',
            },
        ),
        migrations.CreateModel(
            name='WallConstrucion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'wall construcion',
                'verbose_name_plural': 'wall construcions',
            },
        ),
        migrations.CreateModel(
            name='WallFinish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Wall finish',
                'verbose_name_plural': 'Wall finishs',
            },
        ),
        migrations.CreateModel(
            name='Watersupply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'watersupply',
                'verbose_name_plural': 'watersupplies',
            },
        ),
        migrations.CreateModel(
            name='WindowType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'window type',
                'verbose_name_plural': 'window types',
            },
        ),
        migrations.CreateModel(
            name='YandexBuilding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name', db_index=True)),
                ('building_id', models.CharField(max_length=50, verbose_name='Yandex building id', db_index=True)),
                ('ready_quarter', models.IntegerField(verbose_name='Quarter', choices=[(1, '1-\u0439 \u043a\u0432\u0430\u0440\u0442\u0430\u043b'), (2, '2-\u0439 \u043a\u0432\u0430\u0440\u0442\u0430\u043b'), (3, '3-\u0439 \u043a\u0432\u0430\u0440\u0442\u0430\u043b'), (4, '4-\u0439 \u043a\u0432\u0430\u0440\u0442\u0430\u043b')])),
                ('building_state', models.CharField(max_length=15, verbose_name='Building state', choices=[(b'unfinished', '\u0441\u0442\u0440\u043e\u0438\u0442\u0441\u044f'), (b'built', '\u0434\u043e\u043c \u043f\u043e\u0441\u0442\u0440\u043e\u0435\u043d, \u043d\u043e \u043d\u0435 \u0441\u0434\u0430\u043d'), (b'hand-over', '\u0441\u0434\u0430\u043d \u0432 \u044d\u043a\u0441\u043f\u043b\u0443\u0430\u0442\u0430\u0446\u0438\u044e')])),
                ('locality', models.ForeignKey(verbose_name='Locality', blank=True, to='estatebase.Locality', null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'YandexBuilding',
                'verbose_name_plural': 'YandexBuildings',
            },
        ),
        migrations.CreateModel(
            name='ExUser',
            fields=[
            ],
            options={
                'ordering': ['first_name', 'last_name'],
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='street',
            name='street_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='StreetType', to='estatebase.StreetType'),
        ),
        migrations.AddField(
            model_name='office',
            name='head',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Head', blank=True, to='estatebase.ExUser', null=True),
        ),
        migrations.AddField(
            model_name='office',
            name='regions',
            field=models.ManyToManyField(to='estatebase.Region', verbose_name='Region'),
        ),
        migrations.AddField(
            model_name='locality',
            name='locality_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='LocalityType', blank=True, to='estatebase.LocalityType', null=True),
        ),
        migrations.AddField(
            model_name='locality',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Region', blank=True, to='estatebase.Region', null=True),
        ),
        migrations.AddField(
            model_name='level',
            name='level_name',
            field=models.ForeignKey(verbose_name='Level name', to='estatebase.LevelName'),
        ),
        migrations.AddField(
            model_name='layout',
            name='layout_feature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='LayoutFeature', blank=True, to='estatebase.LayoutFeature', null=True),
        ),
        migrations.AddField(
            model_name='layout',
            name='layout_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='LayoutType', to='estatebase.LayoutType'),
        ),
        migrations.AddField(
            model_name='layout',
            name='level',
            field=models.ForeignKey(verbose_name='Level', to='estatebase.Level'),
        ),
        migrations.AddField(
            model_name='historymeta',
            name='created_by',
            field=models.ForeignKey(related_name='creators', on_delete=django.db.models.deletion.PROTECT, verbose_name='User', to='estatebase.ExUser'),
        ),
        migrations.AddField(
            model_name='historymeta',
            name='updated_by',
            field=models.ForeignKey(related_name='updators', on_delete=django.db.models.deletion.PROTECT, verbose_name='Updated by', blank=True, to='estatebase.ExUser', null=True),
        ),
        migrations.AddField(
            model_name='estatetype',
            name='estate_type_category',
            field=models.ForeignKey(related_name='types', on_delete=django.db.models.deletion.PROTECT, verbose_name='EstateTypeCategory', to='estatebase.EstateTypeCategory'),
        ),
        migrations.AddField(
            model_name='estateregister',
            name='history',
            field=models.OneToOneField(null=True, blank=True, editable=False, to='estatebase.HistoryMeta'),
        ),
        migrations.AddField(
            model_name='estateregister',
            name='register_category',
            field=models.ForeignKey(verbose_name='RegisterCategory', blank=True, to='estatebase.RegisterCategory', null=True),
        ),
        migrations.AddField(
            model_name='estateclient',
            name='estate_client_status',
            field=models.ForeignKey(verbose_name='EstateClientStatus', to='estatebase.EstateClientStatus'),
        ),
        migrations.AddField(
            model_name='estate',
            name='broker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Broker', blank=True, to='estatebase.ExUser', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='clients',
            field=models.ManyToManyField(related_name='estates', verbose_name='Clients', through='estatebase.EstateClient', to='estatebase.Client'),
        ),
        migrations.AddField(
            model_name='estate',
            name='com_status',
            field=models.ForeignKey(verbose_name='ComStatus', blank=True, to='estatebase.ComStatus', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Contact', blank=True, to='estatebase.Contact', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='deal_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='DealStatus', blank=True, to='estatebase.DealStatus', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='driveway',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Driveway', blank=True, to='estatebase.Driveway', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='electricity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Electricity', blank=True, to='estatebase.Electricity', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='entrances',
            field=models.ManyToManyField(related_name='estates', to='estatebase.Beside', through='estatebase.EntranceEstate', blank=True, null=True, verbose_name='Entrances'),
        ),
        migrations.AddField(
            model_name='estate',
            name='estate_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='EstateCategory', to='estatebase.EstateTypeCategory'),
        ),
        migrations.AddField(
            model_name='estate',
            name='estate_params',
            field=models.ManyToManyField(related_name='estates', null=True, verbose_name='Estate params', to='estatebase.EstateParam', blank=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='estate_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Estate status', to='estatebase.EstateStatus'),
        ),
        migrations.AddField(
            model_name='estate',
            name='gassupply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Gassupply', blank=True, to='estatebase.Gassupply', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='history',
            field=models.OneToOneField(null=True, blank=True, to='estatebase.HistoryMeta'),
        ),
        migrations.AddField(
            model_name='estate',
            name='internet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Internet', blank=True, to='estatebase.Internet', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='locality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Locality', blank=True, to='estatebase.Locality', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='microdistrict',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Microdistrict', blank=True, to='estatebase.Microdistrict', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Origin', blank=True, to='estatebase.Origin', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Region', to='estatebase.Region'),
        ),
        migrations.AddField(
            model_name='estate',
            name='sewerage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Sewerage', blank=True, to='estatebase.Sewerage', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='street',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Street', blank=True, to='estatebase.Street', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='telephony',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Telephony', blank=True, to='estatebase.Telephony', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='validity',
            field=models.ForeignKey(verbose_name='Validity', blank=True, to='estatebase.Validity', null=True),
        ),
        migrations.AddField(
            model_name='estate',
            name='watersupply',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Watersupply', blank=True, to='estatebase.Watersupply', null=True),
        ),
        migrations.AddField(
            model_name='entranceestate',
            name='estate',
            field=models.ForeignKey(related_name='entranceestate_set', to='estatebase.Estate'),
        ),
        migrations.AddField(
            model_name='document',
            name='estate_type_category',
            field=models.ManyToManyField(to='estatebase.EstateTypeCategory', verbose_name='EstateTypeCategory'),
        ),
        migrations.AddField(
            model_name='contacthistory',
            name='contact_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Contact State', to='estatebase.ContactState'),
        ),
        migrations.AddField(
            model_name='contacthistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='User', blank=True, to='estatebase.ExUser', null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='contact_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=5, verbose_name='Contact State', to='estatebase.ContactState'),
        ),
        migrations.AddField(
            model_name='contact',
            name='contact_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='ContactType', to='estatebase.ContactType'),
        ),
        migrations.AddField(
            model_name='client',
            name='client_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='ClientType', to='estatebase.ClientType'),
        ),
        migrations.AddField(
            model_name='client',
            name='dev_profile',
            field=models.OneToOneField(related_name='client', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='devrep.DevProfile', verbose_name='DevProfile'),
        ),
        migrations.AddField(
            model_name='client',
            name='extra_profile',
            field=models.OneToOneField(related_name='client', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='devrep.ExtraProfile', verbose_name='ExtraProfile'),
        ),
        migrations.AddField(
            model_name='client',
            name='history',
            field=models.OneToOneField(null=True, blank=True, editable=False, to='estatebase.HistoryMeta'),
        ),
        migrations.AddField(
            model_name='client',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Origin', blank=True, to='estatebase.Origin', null=True),
        ),
        migrations.AddField(
            model_name='bidg',
            name='ceiling',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Ceiling', blank=True, to='estatebase.Ceiling', null=True),
        ),
        migrations.AddField(
            model_name='bidg',
            name='documents',
            field=models.ManyToManyField(to='estatebase.Document', null=True, verbose_name='Documents', blank=True),
        ),
        migrations.AddField(
            model_name='bidg',
            name='estate',
            field=models.ForeignKey(related_name='bidgs', verbose_name='Estate', to='estatebase.Estate'),
        ),
        migrations.AddField(
            model_name='bidg',
            name='estate_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='EstateType', to='estatebase.EstateType'),
        ),
        migrations.AddField(
            model_name='bidg',
            name='exterior_finish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Exterior finish', blank=True, to='estatebase.ExteriorFinish', null=True),
        ),
        migrations.AddField(
            model_name='bidg',
            name='flooring',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Flooring', blank=True, to='estatebase.Flooring', null=True),
        ),
        migrations.AddField(
            model_name='bidg',
            name='heating',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Heating', blank=True, to='estatebase.Heating', null=True),
        ),
        migrations.AddField(
            model_name='bidg',
            name='interior',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Interior', blank=True, to='estatebase.Interior', null=True),
        ),
        migrations.AddField(
            model_name='bidg',
            name='roof',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Roof', blank=True, to='estatebase.Roof', null=True),
        ),
        migrations.AddField(
            model_name='bidg',
            name='wall_construcion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Wall construcion', blank=True, to='estatebase.WallConstrucion', null=True),
        ),
        migrations.AddField(
            model_name='bidg',
            name='wall_finish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='WallFinish', blank=True, to='estatebase.WallFinish', null=True),
        ),
        migrations.AddField(
            model_name='bidg',
            name='window_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Window type', blank=True, to='estatebase.WindowType', null=True),
        ),
        migrations.AddField(
            model_name='bidg',
            name='yandex_building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='YandexBuilding', blank=True, to='estatebase.YandexBuilding', null=True),
        ),
        migrations.AddField(
            model_name='bidevent',
            name='bid_event_category',
            field=models.ForeignKey(verbose_name='BidEventCategory', to='estatebase.BidEventCategory'),
        ),
        migrations.AddField(
            model_name='bidevent',
            name='estates',
            field=models.ManyToManyField(to='estatebase.Estate', null=True, verbose_name='Estate', blank=True),
        ),
        migrations.AddField(
            model_name='bidevent',
            name='history',
            field=models.OneToOneField(null=True, blank=True, editable=False, to='estatebase.HistoryMeta'),
        ),
        migrations.AddField(
            model_name='bidclient',
            name='client',
            field=models.ForeignKey(to='estatebase.Client'),
        ),
        migrations.AddField(
            model_name='bid',
            name='bid_status',
            field=models.ManyToManyField(to='estatebase.BidStatus', null=True, verbose_name='BidStatus', blank=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='broker',
            field=models.ForeignKey(related_name='broker_list', on_delete=django.db.models.deletion.PROTECT, verbose_name='User', blank=True, to='estatebase.ExUser', null=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='brokers',
            field=models.ManyToManyField(to='estatebase.ExUser', null=True, verbose_name='User', blank=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='client',
            field=models.ForeignKey(related_name='bids', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Client', blank=True, to='estatebase.Client', null=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='clients',
            field=models.ManyToManyField(related_name='bids_m2m', to='estatebase.Client', through='estatebase.BidClient', blank=True, null=True, verbose_name='Clients'),
        ),
        migrations.AddField(
            model_name='bid',
            name='estate_categories',
            field=models.ManyToManyField(to='estatebase.EstateTypeCategory', null=True, verbose_name='EstateTypeCategory', blank=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='estate_types',
            field=models.ManyToManyField(to='estatebase.EstateType', null=True, verbose_name='Estates types', blank=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='estates',
            field=models.ManyToManyField(to='estatebase.Estate', null=True, verbose_name='Estate', blank=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='geo_groups',
            field=models.ManyToManyField(to='estatebase.GeoGroup', verbose_name='GeoGroups'),
        ),
        migrations.AddField(
            model_name='bid',
            name='history',
            field=models.OneToOneField(null=True, blank=True, editable=False, to='estatebase.HistoryMeta'),
        ),
        migrations.AddField(
            model_name='bid',
            name='localities',
            field=models.ManyToManyField(to='estatebase.Locality', null=True, verbose_name='Locality', blank=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='regions',
            field=models.ManyToManyField(to='estatebase.Region', null=True, verbose_name='Regions', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='street',
            unique_together=set([('name', 'locality', 'street_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='microdistrict',
            unique_together=set([('name', 'locality')]),
        ),
        migrations.AlterUniqueTogether(
            name='locality',
            unique_together=set([('name', 'region')]),
        ),
        migrations.AlterUniqueTogether(
            name='estateclient',
            unique_together=set([('client', 'estate')]),
        ),
        migrations.AlterUniqueTogether(
            name='entranceestate',
            unique_together=set([('beside', 'estate')]),
        ),
        migrations.AlterUniqueTogether(
            name='bidclient',
            unique_together=set([('client', 'bid')]),
        ),
    ]
