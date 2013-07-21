# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WordpressTaxonomyTree.wp_meta_key'
        db.add_column('wp_helper_wordpresstaxonomytree', 'wp_meta_key',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field estate_types on 'WordpressTaxonomyTree'
        db.delete_table(db.shorten_name('wp_helper_wordpresstaxonomytree_estate_types'))

        # Adding M2M table for field regions on 'WordpressTaxonomyTree'
        m2m_table_name = db.shorten_name('wp_helper_wordpresstaxonomytree_regions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordpresstaxonomytree', models.ForeignKey(orm['wp_helper.wordpresstaxonomytree'], null=False)),
            ('region', models.ForeignKey(orm['estatebase.region'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wordpresstaxonomytree_id', 'region_id'])


    def backwards(self, orm):
        # Deleting field 'WordpressTaxonomyTree.wp_meta_key'
        db.delete_column('wp_helper_wordpresstaxonomytree', 'wp_meta_key')

        # Adding M2M table for field estate_types on 'WordpressTaxonomyTree'
        m2m_table_name = db.shorten_name('wp_helper_wordpresstaxonomytree_estate_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordpresstaxonomytree', models.ForeignKey(orm['wp_helper.wordpresstaxonomytree'], null=False)),
            ('estatetype', models.ForeignKey(orm['estatebase.estatetype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wordpresstaxonomytree_id', 'estatetype_id'])

        # Removing M2M table for field regions on 'WordpressTaxonomyTree'
        db.delete_table(db.shorten_name('wp_helper_wordpresstaxonomytree_regions'))


    models = {
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
            'Meta': {'ordering': "['name']", 'object_name': 'WordpressMeta'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'wordpress_meta_type': ('django.db.models.fields.IntegerField', [], {}),
            'wp_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        'wp_helper.wordpresstaxonomytree': {
            'Meta': {'object_name': 'WordpressTaxonomyTree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'localities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['estatebase.Locality']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['wp_helper.WordpressTaxonomyTree']"}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['estatebase.Region']", 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'up_to_date': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wp_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'wp_meta_key': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'wp_parent_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['wp_helper']