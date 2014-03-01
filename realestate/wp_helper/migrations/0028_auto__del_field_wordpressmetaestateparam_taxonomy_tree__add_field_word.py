# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'WordpressMetaEstateParam.taxonomy_tree'
        db.delete_column('wp_helper_wordpressmetaestateparam', 'taxonomy_tree_id')

        # Adding field 'WordpressMetaEstateParam.wp_taxonomy_tree'
        db.add_column('wp_helper_wordpressmetaestateparam', 'wp_taxonomy_tree',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wp_helper.WordpressTaxonomyTree'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'WordpressMetaEstateParam.taxonomy_tree'
        db.add_column('wp_helper_wordpressmetaestateparam', 'taxonomy_tree',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wp_helper.WordpressTaxonomyTree'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'WordpressMetaEstateParam.wp_taxonomy_tree'
        db.delete_column('wp_helper_wordpressmetaestateparam', 'wp_taxonomy_tree_id')


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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'name_gent': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_loct': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'estatebase.client': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'client_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.ClientType']", 'on_delete': 'models.PROTECT'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'history': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['estatebase.HistoryMeta']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Origin']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'})
        },
        'estatebase.clienttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ClientType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.comstatus': {
            'Meta': {'ordering': "['name']", 'object_name': 'ComStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {})
        },
        'estatebase.contact': {
            'Meta': {'ordering': "['contact_state__id', 'contact_type__id']", 'object_name': 'Contact'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['estatebase.Client']"}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'contact_state': ('django.db.models.fields.related.ForeignKey', [], {'default': '5', 'to': "orm['estatebase.ContactState']", 'on_delete': 'models.PROTECT'}),
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.ContactType']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'estatebase.contactstate': {
            'Meta': {'ordering': "['name']", 'object_name': 'ContactState'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.contacttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ContactType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.driveway': {
            'Meta': {'ordering': "['name']", 'object_name': 'Driveway'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.electricity': {
            'Meta': {'ordering': "['name']", 'object_name': 'Electricity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.estate': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Estate'},
            'agency_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'beside': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Beside']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'beside_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'broker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'client_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'clients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'estates'", 'symmetrical': 'False', 'through': "orm['estatebase.EstateClient']", 'to': "orm['estatebase.Client']"}),
            'com_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.ComStatus']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Contact']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'driveway': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Driveway']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'driveway_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'electricity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Electricity']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'electricity_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'estate_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.EstateTypeCategory']", 'on_delete': 'models.PROTECT'}),
            'estate_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'estate_params': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'estates'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['estatebase.EstateParam']"}),
            'estate_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.EstateStatus']", 'on_delete': 'models.PROTECT'}),
            'gassupply': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Gassupply']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'gassupply_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'history': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['estatebase.HistoryMeta']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Internet']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'microdistrict': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Microdistrict']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Origin']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Region']", 'on_delete': 'models.PROTECT'}),
            'saler_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sewerage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Sewerage']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'sewerage_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Street']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'telephony': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Telephony']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'validity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Validity']", 'null': 'True', 'blank': 'True'}),
            'watersupply': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Watersupply']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'watersupply_distance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'estatebase.estateclient': {
            'Meta': {'unique_together': "(('client', 'estate'),)", 'object_name': 'EstateClient'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Client']"}),
            'estate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Estate']"}),
            'estate_client_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.EstateClientStatus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'estatebase.estateclientstatus': {
            'Meta': {'ordering': "['name']", 'object_name': 'EstateClientStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.estateparam': {
            'Meta': {'ordering': "['order']", 'object_name': 'EstateParam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'})
        },
        'estatebase.estatestatus': {
            'Meta': {'ordering': "['name']", 'object_name': 'EstateStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.estatetype': {
            'Meta': {'ordering': "['estate_type_category__order', 'name']", 'object_name': 'EstateType'},
            'estate_type_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'types'", 'on_delete': 'models.PROTECT', 'to': "orm['estatebase.EstateTypeCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_accs': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'}),
            'placeable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'template': ('django.db.models.fields.IntegerField', [], {})
        },
        'estatebase.estatetypecategory': {
            'Meta': {'ordering': "['order']", 'object_name': 'EstateTypeCategory'},
            'has_bidg': ('django.db.models.fields.IntegerField', [], {}),
            'has_stead': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'independent': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_commerce': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'})
        },
        'estatebase.gassupply': {
            'Meta': {'ordering': "['name']", 'object_name': 'Gassupply'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.geogroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'GeoGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.historymeta': {
            'Meta': {'object_name': 'HistoryMeta'},
            'created': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creators'", 'on_delete': 'models.PROTECT', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modificated': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updators'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['auth.User']"})
        },
        'estatebase.internet': {
            'Meta': {'ordering': "['name']", 'object_name': 'Internet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.locality': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'region'),)", 'object_name': 'Locality'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.LocalityType']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'name_gent': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_loct': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Region']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'})
        },
        'estatebase.localitytype': {
            'Meta': {'ordering': "['name']", 'object_name': 'LocalityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'prep_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.microdistrict': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'locality'),)", 'object_name': 'Microdistrict'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']", 'on_delete': 'models.PROTECT'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.origin': {
            'Meta': {'ordering': "['name']", 'object_name': 'Origin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.region': {
            'Meta': {'ordering': "['name']", 'object_name': 'Region'},
            'geo_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.GeoGroup']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'regular_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'regular_name_gent': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'estatebase.sewerage': {
            'Meta': {'ordering': "['name']", 'object_name': 'Sewerage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.street': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'locality'),)", 'object_name': 'Street'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']", 'on_delete': 'models.PROTECT'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.telephony': {
            'Meta': {'ordering': "['name']", 'object_name': 'Telephony'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.validity': {
            'Meta': {'ordering': "['name']", 'object_name': 'Validity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.watersupply': {
            'Meta': {'ordering': "['name']", 'object_name': 'Watersupply'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'wp_helper.estatewordpressmeta': {
            'Meta': {'object_name': 'EstateWordpressMeta'},
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'estate': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'wp_meta'", 'unique': 'True', 'to': "orm['estatebase.Estate']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'unique': 'True', 'null': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'wp_helper.wordpressmeta': {
            'Meta': {'object_name': 'WordpressMeta'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'wp_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'blank': 'True'})
        },
        'wp_helper.wordpressmetaestateparam': {
            'Meta': {'ordering': "['name']", 'object_name': 'WordpressMetaEstateParam'},
            'estate_params': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'wp_taxons'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['estatebase.EstateParam']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'wp_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'blank': 'True'}),
            'wp_taxonomy_tree': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wp_helper.WordpressTaxonomyTree']", 'null': 'True', 'blank': 'True'})
        },
        'wp_helper.wordpressmetaestatetype': {
            'Meta': {'ordering': "['name']", 'object_name': 'WordpressMetaEstateType'},
            'estate_types': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'wp_taxons'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['estatebase.EstateType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'wp_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'blank': 'True'})
        },
        'wp_helper.wordpressmetaregion': {
            'Meta': {'ordering': "['name']", 'object_name': 'WordpressMetaRegion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'wp_taxons'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['estatebase.Region']"}),
            'wp_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'blank': 'True'})
        },
        'wp_helper.wordpressmetastatus': {
            'Meta': {'ordering': "['name']", 'object_name': 'WordpressMetaStatus'},
            'estate_statuses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'wp_taxons'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['estatebase.EstateStatus']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'wp_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'blank': 'True'})
        },
        'wp_helper.wordpresstaxonomytree': {
            'Meta': {'object_name': 'WordpressTaxonomyTree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'localities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'wp_taxons'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['estatebase.Locality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['wp_helper.WordpressTaxonomyTree']"}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['estatebase.Region']", 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'up_to_date': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wp_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'wp_meta_locality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'wp_taxon'", 'null': 'True', 'to': "orm['wp_helper.WordpressMeta']"}),
            'wp_parent_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['wp_helper']