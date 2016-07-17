# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BaseFeed.engine_mapper'
        db.add_column('exportdata_basefeed', 'engine_mapper',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exportdata.EngineMapper'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BaseFeed.engine_mapper'
        db.delete_column('exportdata_basefeed', 'engine_mapper_id')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'estatebase.estateparam': {
            'Meta': {'ordering': "['order']", 'object_name': 'EstateParam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'blank': 'True'})
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
        'estatebase.geogroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'GeoGroup'},
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
            'prep_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'sort_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'estatebase.region': {
            'Meta': {'ordering': "['name']", 'object_name': 'Region'},
            'geo_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.GeoGroup']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metropolis': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'metropolis_region'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['estatebase.Locality']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'regular_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'regular_name_gent': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'exportdata.basefeed': {
            'Meta': {'object_name': 'BaseFeed'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exportdata.MarketingCampaign']", 'null': 'True', 'blank': 'True'}),
            'engine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exportdata.FeedEngine']", 'null': 'True', 'blank': 'True'}),
            'engine_mapper': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exportdata.EngineMapper']", 'null': 'True', 'blank': 'True'}),
            'estate_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['estatebase.EstateTypeCategory']", 'symmetrical': 'False'}),
            'estate_params': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['estatebase.EstateParam']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'valid_days': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'exportdata.enginemapper': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'engine'),)", 'object_name': 'EngineMapper'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'on_delete': 'models.PROTECT'}),
            'engine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exportdata.FeedEngine']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'xml_value': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'exportdata.feedcontenttype': {
            'Meta': {'object_name': 'FeedContentType'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'on_delete': 'models.PROTECT'}),
            'feeds': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['exportdata.BaseFeed']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'exportdata.feedengine': {
            'Meta': {'object_name': 'FeedEngine'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'})
        },
        'exportdata.feedlocality': {
            'Meta': {'ordering': "['locality']", 'unique_together': "(('feed_code', 'locality'),)", 'object_name': 'FeedLocality'},
            'feed_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'feed_name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']", 'on_delete': 'models.PROTECT'})
        },
        'exportdata.marketingcampaign': {
            'Meta': {'object_name': 'MarketingCampaign'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'feeds': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['exportdata.BaseFeed']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 7, 2, 0, 0)'})
        }
    }

    complete_apps = ['exportdata']