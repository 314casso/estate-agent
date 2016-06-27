# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'FeedMapper', fields ['content_type', 'object_id', 'feed']
        db.create_unique('exportdata_feedmapper', ['content_type_id', 'object_id', 'feed_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'FeedMapper', fields ['content_type', 'object_id', 'feed']
        db.delete_unique('exportdata_feedmapper', ['content_type_id', 'object_id', 'feed_id'])


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'rules_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'exportdata.feedcontenttype': {
            'Meta': {'object_name': 'FeedContentType'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'on_delete': 'models.PROTECT'}),
            'feeds': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['exportdata.BaseFeed']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'exportdata.feedlocality': {
            'Meta': {'ordering': "['locality']", 'unique_together': "(('feed_code', 'locality'),)", 'object_name': 'FeedLocality'},
            'feed_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'feed_name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']", 'on_delete': 'models.PROTECT'})
        },
        'exportdata.feedmapper': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'feed'),)", 'object_name': 'FeedMapper'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'on_delete': 'models.PROTECT'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exportdata.BaseFeed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'xml_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['exportdata']