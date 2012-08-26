# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Bid.client'
        db.add_column('estatebase_bid', 'client',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='bids', to=orm['estatebase.Client']),
                      keep_default=False)

        # Removing M2M table for field estate on 'Bid'
        db.delete_table('estatebase_bid_estate')

        # Removing M2M table for field estate_type on 'Bid'
        db.delete_table('estatebase_bid_estate_type')

        # Removing M2M table for field localitie on 'Bid'
        db.delete_table('estatebase_bid_localitie')

        # Removing M2M table for field region on 'Bid'
        db.delete_table('estatebase_bid_region')

        # Removing M2M table for field contact on 'Bid'
        db.delete_table('estatebase_bid_contact')

        # Removing M2M table for field client on 'Bid'
        db.delete_table('estatebase_bid_client')

        # Adding M2M table for field estates on 'Bid'
        db.create_table('estatebase_bid_estates', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bid', models.ForeignKey(orm['estatebase.bid'], null=False)),
            ('estate', models.ForeignKey(orm['estatebase.estate'], null=False))
        ))
        db.create_unique('estatebase_bid_estates', ['bid_id', 'estate_id'])

        # Adding M2M table for field clients on 'Bid'
        db.create_table('estatebase_bid_clients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bid', models.ForeignKey(orm['estatebase.bid'], null=False)),
            ('client', models.ForeignKey(orm['estatebase.client'], null=False))
        ))
        db.create_unique('estatebase_bid_clients', ['bid_id', 'client_id'])

        # Adding M2M table for field contacts on 'Bid'
        db.create_table('estatebase_bid_contacts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bid', models.ForeignKey(orm['estatebase.bid'], null=False)),
            ('contact', models.ForeignKey(orm['estatebase.contact'], null=False))
        ))
        db.create_unique('estatebase_bid_contacts', ['bid_id', 'contact_id'])

        # Adding M2M table for field estate_types on 'Bid'
        db.create_table('estatebase_bid_estate_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bid', models.ForeignKey(orm['estatebase.bid'], null=False)),
            ('estatetype', models.ForeignKey(orm['estatebase.estatetype'], null=False))
        ))
        db.create_unique('estatebase_bid_estate_types', ['bid_id', 'estatetype_id'])

        # Adding M2M table for field regions on 'Bid'
        db.create_table('estatebase_bid_regions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bid', models.ForeignKey(orm['estatebase.bid'], null=False)),
            ('region', models.ForeignKey(orm['estatebase.region'], null=False))
        ))
        db.create_unique('estatebase_bid_regions', ['bid_id', 'region_id'])

        # Adding M2M table for field localities on 'Bid'
        db.create_table('estatebase_bid_localities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bid', models.ForeignKey(orm['estatebase.bid'], null=False)),
            ('locality', models.ForeignKey(orm['estatebase.locality'], null=False))
        ))
        db.create_unique('estatebase_bid_localities', ['bid_id', 'locality_id'])


    def backwards(self, orm):
        # Deleting field 'Bid.client'
        db.delete_column('estatebase_bid', 'client_id')

        # Adding M2M table for field estate on 'Bid'
        db.create_table('estatebase_bid_estate', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bid', models.ForeignKey(orm['estatebase.bid'], null=False)),
            ('estate', models.ForeignKey(orm['estatebase.estate'], null=False))
        ))
        db.create_unique('estatebase_bid_estate', ['bid_id', 'estate_id'])

        # Adding M2M table for field estate_type on 'Bid'
        db.create_table('estatebase_bid_estate_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bid', models.ForeignKey(orm['estatebase.bid'], null=False)),
            ('estatetype', models.ForeignKey(orm['estatebase.estatetype'], null=False))
        ))
        db.create_unique('estatebase_bid_estate_type', ['bid_id', 'estatetype_id'])

        # Adding M2M table for field localitie on 'Bid'
        db.create_table('estatebase_bid_localitie', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bid', models.ForeignKey(orm['estatebase.bid'], null=False)),
            ('locality', models.ForeignKey(orm['estatebase.locality'], null=False))
        ))
        db.create_unique('estatebase_bid_localitie', ['bid_id', 'locality_id'])

        # Adding M2M table for field region on 'Bid'
        db.create_table('estatebase_bid_region', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bid', models.ForeignKey(orm['estatebase.bid'], null=False)),
            ('region', models.ForeignKey(orm['estatebase.region'], null=False))
        ))
        db.create_unique('estatebase_bid_region', ['bid_id', 'region_id'])

        # Adding M2M table for field contact on 'Bid'
        db.create_table('estatebase_bid_contact', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bid', models.ForeignKey(orm['estatebase.bid'], null=False)),
            ('contact', models.ForeignKey(orm['estatebase.contact'], null=False))
        ))
        db.create_unique('estatebase_bid_contact', ['bid_id', 'contact_id'])

        # Adding M2M table for field client on 'Bid'
        db.create_table('estatebase_bid_client', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bid', models.ForeignKey(orm['estatebase.bid'], null=False)),
            ('client', models.ForeignKey(orm['estatebase.client'], null=False))
        ))
        db.create_unique('estatebase_bid_client', ['bid_id', 'client_id'])

        # Removing M2M table for field estates on 'Bid'
        db.delete_table('estatebase_bid_estates')

        # Removing M2M table for field clients on 'Bid'
        db.delete_table('estatebase_bid_clients')

        # Removing M2M table for field contacts on 'Bid'
        db.delete_table('estatebase_bid_contacts')

        # Removing M2M table for field estate_types on 'Bid'
        db.delete_table('estatebase_bid_estate_types')

        # Removing M2M table for field regions on 'Bid'
        db.delete_table('estatebase_bid_regions')

        # Removing M2M table for field localities on 'Bid'
        db.delete_table('estatebase_bid_localities')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'estatebase.beside': {
            'Meta': {'ordering': "['name']", 'object_name': 'Beside'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.bid': {
            'Meta': {'object_name': 'Bid'},
            'agency_price_max': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'agency_price_min': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'broker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'brokers'", 'null': 'True', 'to': "orm['auth.User']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bids'", 'to': "orm['estatebase.Client']"}),
            'clients': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['estatebase.Client']", 'null': 'True', 'blank': 'True'}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['estatebase.Contact']", 'null': 'True', 'blank': 'True'}),
            'estate_filter': ('picklefield.fields.PickledObjectField', [], {'null': 'True', 'blank': 'True'}),
            'estate_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['estatebase.EstateType']", 'null': 'True', 'blank': 'True'}),
            'estates': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['estatebase.Estate']", 'null': 'True', 'blank': 'True'}),
            'history': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['estatebase.HistoryMeta']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['estatebase.Locality']", 'null': 'True', 'blank': 'True'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['estatebase.Region']", 'null': 'True', 'blank': 'True'})
        },
        'estatebase.bidg': {
            'Meta': {'ordering': "['id']", 'object_name': 'Bidg'},
            'basic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ceiling': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Ceiling']", 'null': 'True', 'blank': 'True'}),
            'ceiling_height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'documents': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['estatebase.Document']", 'null': 'True', 'blank': 'True'}),
            'elevator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'estate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bidgs'", 'to': "orm['estatebase.Estate']"}),
            'estate_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.EstateType']"}),
            'exterior_finish': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.ExteriorFinish']", 'null': 'True', 'blank': 'True'}),
            'floor': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'floor_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'flooring': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Flooring']", 'null': 'True', 'blank': 'True'}),
            'heating': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Heating']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interior': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Interior']", 'null': 'True', 'blank': 'True'}),
            'roof': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Roof']", 'null': 'True', 'blank': 'True'}),
            'room_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'room_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'total_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'used_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'wall_construcion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.WallConstrucion']", 'null': 'True', 'blank': 'True'}),
            'wall_finish': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.WallFinish']", 'null': 'True', 'blank': 'True'}),
            'window_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.WindowType']", 'null': 'True', 'blank': 'True'}),
            'year_built': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'estatebase.ceiling': {
            'Meta': {'ordering': "['name']", 'object_name': 'Ceiling'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.client': {
            'Meta': {'ordering': "['id']", 'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'client_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.ClientType']"}),
            'history': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['estatebase.HistoryMeta']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Origin']", 'null': 'True', 'blank': 'True'})
        },
        'estatebase.clienttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ClientType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.contact': {
            'Meta': {'ordering': "['contact_type__pk']", 'object_name': 'Contact'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['estatebase.Client']"}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'contact_state': ('django.db.models.fields.related.ForeignKey', [], {'default': '5', 'to': "orm['estatebase.ContactState']"}),
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.ContactType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'estatebase.contacthistory': {
            'Meta': {'object_name': 'ContactHistory'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Contact']"}),
            'contact_state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.ContactState']"}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 25, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'estatebase.contactstate': {
            'Meta': {'ordering': "['name']", 'object_name': 'ContactState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.contacttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ContactType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.document': {
            'Meta': {'ordering': "['name']", 'object_name': 'Document'},
            'estate_type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['estatebase.EstateType']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.driveway': {
            'Meta': {'ordering': "['name']", 'object_name': 'Driveway'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.electricity': {
            'Meta': {'ordering': "['name']", 'object_name': 'Electricity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.estate': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Estate'},
            'agency_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'beside': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Beside']", 'null': 'True', 'blank': 'True'}),
            'beside_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'clients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'estates'", 'symmetrical': 'False', 'to': "orm['estatebase.Client']"}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Contact']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'driveway': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Driveway']", 'null': 'True', 'blank': 'True'}),
            'driveway_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'electricity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Electricity']", 'null': 'True', 'blank': 'True'}),
            'electricity_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'estate_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'estate_params': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['estatebase.EstateParam']", 'null': 'True', 'blank': 'True'}),
            'estate_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.EstateStatus']"}),
            'estate_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.EstateType']"}),
            'gassupply': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Gassupply']", 'null': 'True', 'blank': 'True'}),
            'gassupply_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'history': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['estatebase.HistoryMeta']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Internet']", 'null': 'True', 'blank': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']"}),
            'microdistrict': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Microdistrict']", 'null': 'True', 'blank': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Origin']", 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Region']", 'null': 'True', 'blank': 'True'}),
            'saler_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sewerage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Sewerage']", 'null': 'True', 'blank': 'True'}),
            'sewerage_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Street']"}),
            'telephony': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Telephony']", 'null': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'watersupply': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Watersupply']", 'null': 'True', 'blank': 'True'}),
            'watersupply_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'estatebase.estateparam': {
            'Meta': {'ordering': "['order']", 'object_name': 'EstateParam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'})
        },
        'estatebase.estatephoto': {
            'Meta': {'ordering': "['order']", 'object_name': 'EstatePhoto'},
            'estate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['estatebase.Estate']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'})
        },
        'estatebase.estatestatus': {
            'Meta': {'ordering': "['name']", 'object_name': 'EstateStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.estatetype': {
            'Meta': {'ordering': "['name']", 'object_name': 'EstateType'},
            'estate_type_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.EstateTypeCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'object_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'}),
            'placeable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'estatebase.estatetypecategory': {
            'Meta': {'ordering': "['order']", 'object_name': 'EstateTypeCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'})
        },
        'estatebase.exteriorfinish': {
            'Meta': {'ordering': "['name']", 'object_name': 'ExteriorFinish'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.flooring': {
            'Meta': {'ordering': "['name']", 'object_name': 'Flooring'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.furniture': {
            'Meta': {'ordering': "['name']", 'object_name': 'Furniture'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.gassupply': {
            'Meta': {'ordering': "['name']", 'object_name': 'Gassupply'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.geogroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'GeoGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.heating': {
            'Meta': {'ordering': "['name']", 'object_name': 'Heating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.historymeta': {
            'Meta': {'object_name': 'HistoryMeta'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creators'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updators'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'estatebase.interior': {
            'Meta': {'ordering': "['name']", 'object_name': 'Interior'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.internet': {
            'Meta': {'ordering': "['name']", 'object_name': 'Internet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.landtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'LandType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.layout': {
            'Meta': {'object_name': 'Layout'},
            'area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'furniture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Furniture']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layout_feature': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.LayoutFeature']", 'null': 'True', 'blank': 'True'}),
            'layout_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.LayoutType']"}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Level']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'estatebase.layoutfeature': {
            'Meta': {'ordering': "['name']", 'object_name': 'LayoutFeature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.layouttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'LayoutType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.level': {
            'Meta': {'ordering': "['level_name']", 'object_name': 'Level'},
            'bidg': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'levels'", 'to': "orm['estatebase.Bidg']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.LevelName']"})
        },
        'estatebase.levelname': {
            'Meta': {'ordering': "['name']", 'object_name': 'LevelName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.locality': {
            'Meta': {'ordering': "['name']", 'object_name': 'Locality'},
            'geo_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.GeoGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Region']", 'null': 'True', 'blank': 'True'})
        },
        'estatebase.microdistrict': {
            'Meta': {'ordering': "['name']", 'object_name': 'Microdistrict'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.origin': {
            'Meta': {'ordering': "['name']", 'object_name': 'Origin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.purpose': {
            'Meta': {'ordering': "['name']", 'object_name': 'Purpose'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.region': {
            'Meta': {'ordering': "['name']", 'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.roof': {
            'Meta': {'ordering': "['name']", 'object_name': 'Roof'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.sewerage': {
            'Meta': {'ordering': "['name']", 'object_name': 'Sewerage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.shape': {
            'Meta': {'ordering': "['name']", 'object_name': 'Shape'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.stead': {
            'Meta': {'object_name': 'Stead'},
            'estate': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'stead'", 'unique': 'True', 'to': "orm['estatebase.Estate']"}),
            'face_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.LandType']", 'null': 'True', 'blank': 'True'}),
            'purpose': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Purpose']", 'null': 'True', 'blank': 'True'}),
            'shape': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Shape']", 'null': 'True', 'blank': 'True'}),
            'total_area': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'})
        },
        'estatebase.street': {
            'Meta': {'ordering': "['name']", 'object_name': 'Street'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.telephony': {
            'Meta': {'ordering': "['name']", 'object_name': 'Telephony'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'geo_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['estatebase.GeoGroup']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'estatebase.wallconstrucion': {
            'Meta': {'ordering': "['name']", 'object_name': 'WallConstrucion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.wallfinish': {
            'Meta': {'ordering': "['name']", 'object_name': 'WallFinish'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.watersupply': {
            'Meta': {'ordering': "['name']", 'object_name': 'Watersupply'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.windowtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'WindowType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['estatebase']