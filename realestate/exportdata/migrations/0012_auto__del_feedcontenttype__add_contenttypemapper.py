# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'FeedContentType'
        db.delete_table('exportdata_feedcontenttype')

        # Removing M2M table for field feeds on 'FeedContentType'
        db.delete_table(db.shorten_name('exportdata_feedcontenttype_feeds'))

        # Adding model 'ContentTypeMapper'
        db.create_table('exportdata_contenttypemapper', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], on_delete=models.PROTECT)),
        ))
        db.send_create_signal('exportdata', ['ContentTypeMapper'])

        # Adding M2M table for field mapper_engine on 'ContentTypeMapper'
        m2m_table_name = db.shorten_name('exportdata_contenttypemapper_mapper_engine')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contenttypemapper', models.ForeignKey(orm['exportdata.contenttypemapper'], null=False)),
            ('mapperengine', models.ForeignKey(orm['exportdata.mapperengine'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contenttypemapper_id', 'mapperengine_id'])


    def backwards(self, orm):
        # Adding model 'FeedContentType'
        db.create_table('exportdata_feedcontenttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], on_delete=models.PROTECT)),
        ))
        db.send_create_signal('exportdata', ['FeedContentType'])

        # Adding M2M table for field feeds on 'FeedContentType'
        m2m_table_name = db.shorten_name('exportdata_feedcontenttype_feeds')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feedcontenttype', models.ForeignKey(orm['exportdata.feedcontenttype'], null=False)),
            ('basefeed', models.ForeignKey(orm['exportdata.basefeed'], null=False))
        ))
        db.create_unique(m2m_table_name, ['feedcontenttype_id', 'basefeed_id'])

        # Deleting model 'ContentTypeMapper'
        db.delete_table('exportdata_contenttypemapper')

        # Removing M2M table for field mapper_engine on 'ContentTypeMapper'
        db.delete_table(db.shorten_name('exportdata_contenttypemapper_mapper_engine'))


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
            'estate_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['estatebase.EstateTypeCategory']", 'symmetrical': 'False'}),
            'estate_params': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['estatebase.EstateParam']", 'symmetrical': 'False'}),
            'feed_engine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exportdata.FeedEngine']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapper_engine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exportdata.MapperEngine']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'valid_days': ('django.db.models.fields.IntegerField', [], {})
        },
        'exportdata.contenttypemapper': {
            'Meta': {'object_name': 'ContentTypeMapper'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapper_engine': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['exportdata.MapperEngine']", 'symmetrical': 'False'})
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
        'exportdata.mapperengine': {
            'Meta': {'object_name': 'MapperEngine'},
            'feed_engine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exportdata.FeedEngine']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
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
        },
        'exportdata.valuemapper': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'mapper_engine'),)", 'object_name': 'ValueMapper'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapper_engine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exportdata.MapperEngine']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'xml_value': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['exportdata']