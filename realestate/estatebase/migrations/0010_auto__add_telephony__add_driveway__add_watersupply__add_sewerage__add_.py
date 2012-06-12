# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Telephony'
        db.create_table('estatebase_telephony', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('estatebase', ['Telephony'])

        # Adding model 'Driveway'
        db.create_table('estatebase_driveway', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('estatebase', ['Driveway'])

        # Adding model 'Watersupply'
        db.create_table('estatebase_watersupply', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('estatebase', ['Watersupply'])

        # Adding model 'Sewerage'
        db.create_table('estatebase_sewerage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('estatebase', ['Sewerage'])

        # Adding model 'Gassupply'
        db.create_table('estatebase_gassupply', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('estatebase', ['Gassupply'])

        # Adding model 'Electricity'
        db.create_table('estatebase_electricity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('estatebase', ['Electricity'])

        # Adding model 'Internet'
        db.create_table('estatebase_internet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('estatebase', ['Internet'])

        # Adding field 'Estate.electricity'
        db.add_column('estatebase_estate', 'electricity',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Electricity'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Estate.electricity_distance'
        db.add_column('estatebase_estate', 'electricity_distance',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Estate.watersupply'
        db.add_column('estatebase_estate', 'watersupply',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Watersupply'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Estate.watersupply_distance'
        db.add_column('estatebase_estate', 'watersupply_distance',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Estate.gassupply'
        db.add_column('estatebase_estate', 'gassupply',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Gassupply'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Estate.gassupply_distance'
        db.add_column('estatebase_estate', 'gassupply_distance',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Estate.sewerage'
        db.add_column('estatebase_estate', 'sewerage',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Sewerage'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Estate.sewerage_distance'
        db.add_column('estatebase_estate', 'sewerage_distance',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Estate.telephony'
        db.add_column('estatebase_estate', 'telephony',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Telephony'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Estate.internet'
        db.add_column('estatebase_estate', 'internet',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Internet'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Estate.driveway'
        db.add_column('estatebase_estate', 'driveway',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Driveway'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Estate.driveway_distance'
        db.add_column('estatebase_estate', 'driveway_distance',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Telephony'
        db.delete_table('estatebase_telephony')

        # Deleting model 'Driveway'
        db.delete_table('estatebase_driveway')

        # Deleting model 'Watersupply'
        db.delete_table('estatebase_watersupply')

        # Deleting model 'Sewerage'
        db.delete_table('estatebase_sewerage')

        # Deleting model 'Gassupply'
        db.delete_table('estatebase_gassupply')

        # Deleting model 'Electricity'
        db.delete_table('estatebase_electricity')

        # Deleting model 'Internet'
        db.delete_table('estatebase_internet')

        # Deleting field 'Estate.electricity'
        db.delete_column('estatebase_estate', 'electricity_id')

        # Deleting field 'Estate.electricity_distance'
        db.delete_column('estatebase_estate', 'electricity_distance')

        # Deleting field 'Estate.watersupply'
        db.delete_column('estatebase_estate', 'watersupply_id')

        # Deleting field 'Estate.watersupply_distance'
        db.delete_column('estatebase_estate', 'watersupply_distance')

        # Deleting field 'Estate.gassupply'
        db.delete_column('estatebase_estate', 'gassupply_id')

        # Deleting field 'Estate.gassupply_distance'
        db.delete_column('estatebase_estate', 'gassupply_distance')

        # Deleting field 'Estate.sewerage'
        db.delete_column('estatebase_estate', 'sewerage_id')

        # Deleting field 'Estate.sewerage_distance'
        db.delete_column('estatebase_estate', 'sewerage_distance')

        # Deleting field 'Estate.telephony'
        db.delete_column('estatebase_estate', 'telephony_id')

        # Deleting field 'Estate.internet'
        db.delete_column('estatebase_estate', 'internet_id')

        # Deleting field 'Estate.driveway'
        db.delete_column('estatebase_estate', 'driveway_id')

        # Deleting field 'Estate.driveway_distance'
        db.delete_column('estatebase_estate', 'driveway_distance')


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
        'estatebase.bidg': {
            'Meta': {'object_name': 'Bidg', '_ormbases': ['estatebase.Estate']},
            'estate_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['estatebase.Estate']", 'unique': 'True', 'primary_key': 'True'}),
            'room_number': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'estatebase.client': {
            'Meta': {'ordering': "['id']", 'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'client_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.ClientType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creators'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Origin']", 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updaters'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'estatebase.clienttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ClientType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.contact': {
            'Meta': {'ordering': "['contact_type__pk']", 'object_name': 'Contact'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contactlist'", 'to': "orm['estatebase.Client']"}),
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
            'event_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 12, 0, 0)'}),
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
            'Meta': {'object_name': 'Estate'},
            'agency_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'beside': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Beside']", 'null': 'True', 'blank': 'True'}),
            'beside_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'clients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'estates'", 'symmetrical': 'False', 'to': "orm['estatebase.Client']"}),
            'driveway': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Driveway']", 'null': 'True', 'blank': 'True'}),
            'driveway_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'electricity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Electricity']", 'null': 'True', 'blank': 'True'}),
            'electricity_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'estate_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.EstateType']", 'null': 'True', 'blank': 'True'}),
            'gassupply': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Gassupply']", 'null': 'True', 'blank': 'True'}),
            'gassupply_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'watersupply': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Watersupply']", 'null': 'True', 'blank': 'True'}),
            'watersupply_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'estatebase.estatetype': {
            'Meta': {'ordering': "['order']", 'object_name': 'EstateType'},
            'estate_type_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.EstateTypeCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'object_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'})
        },
        'estatebase.estatetypecategory': {
            'Meta': {'ordering': "['order']", 'object_name': 'EstateTypeCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'})
        },
        'estatebase.gassupply': {
            'Meta': {'ordering': "['name']", 'object_name': 'Gassupply'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.internet': {
            'Meta': {'ordering': "['name']", 'object_name': 'Internet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.locality': {
            'Meta': {'ordering': "['name']", 'object_name': 'Locality'},
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
        'estatebase.region': {
            'Meta': {'ordering': "['name']", 'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.sewerage': {
            'Meta': {'ordering': "['name']", 'object_name': 'Sewerage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        'estatebase.watersupply': {
            'Meta': {'ordering': "['name']", 'object_name': 'Watersupply'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['estatebase']