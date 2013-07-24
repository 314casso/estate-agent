# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field estate_types on 'WordpressMetaEstateType'
        m2m_table_name = db.shorten_name('wp_helper_wordpressmetaestatetype_estate_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordpressmetaestatetype', models.ForeignKey(orm['wp_helper.wordpressmetaestatetype'], null=False)),
            ('estatetype', models.ForeignKey(orm['estatebase.estatetype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wordpressmetaestatetype_id', 'estatetype_id'])


    def backwards(self, orm):
        # Removing M2M table for field estate_types on 'WordpressMetaEstateType'
        db.delete_table(db.shorten_name('wp_helper_wordpressmetaestatetype_estate_types'))


    models = {
        'estatebase.estatetype': {
            'Meta': {'ordering': "['estate_type_category__order', 'name']", 'object_name': 'EstateType'},
            'estate_type_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'types'", 'on_delete': 'models.PROTECT', 'to': "orm['estatebase.EstateTypeCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Region']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'})
        },
        'estatebase.localitytype': {
            'Meta': {'ordering': "['name']", 'object_name': 'LocalityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'prep_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.region': {
            'Meta': {'ordering': "['name']", 'object_name': 'Region'},
            'geo_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.GeoGroup']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'wp_helper.wordpressmeta': {
            'Meta': {'object_name': 'WordpressMeta'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'wp_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'blank': 'True'})
        },
        'wp_helper.wordpressmetaestatetype': {
            'Meta': {'object_name': 'WordpressMetaEstateType'},
            'estate_types': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'wp_taxons'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['estatebase.EstateType']"}),
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
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'wp_taxons'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['estatebase.Region']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'up_to_date': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wp_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'wp_meta_locality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'wp_taxon'", 'null': 'True', 'to': "orm['wp_helper.WordpressMeta']"}),
            'wp_parent_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['wp_helper']