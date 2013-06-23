# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WordpressTaxonomyTree.lft'
        db.add_column('wp_helper_wordpresstaxonomytree', 'lft',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)

        # Adding field 'WordpressTaxonomyTree.rght'
        db.add_column('wp_helper_wordpresstaxonomytree', 'rght',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)

        # Adding field 'WordpressTaxonomyTree.tree_id'
        db.add_column('wp_helper_wordpresstaxonomytree', 'tree_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)

        # Adding field 'WordpressTaxonomyTree.level'
        db.add_column('wp_helper_wordpresstaxonomytree', 'level',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WordpressTaxonomyTree.lft'
        db.delete_column('wp_helper_wordpresstaxonomytree', 'lft')

        # Deleting field 'WordpressTaxonomyTree.rght'
        db.delete_column('wp_helper_wordpresstaxonomytree', 'rght')

        # Deleting field 'WordpressTaxonomyTree.tree_id'
        db.delete_column('wp_helper_wordpresstaxonomytree', 'tree_id')

        # Deleting field 'WordpressTaxonomyTree.level'
        db.delete_column('wp_helper_wordpresstaxonomytree', 'level')


    models = {
        'wp_helper.wordpresstaxonomytree': {
            'Meta': {'object_name': 'WordpressTaxonomyTree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['wp_helper.WordpressTaxonomyTree']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'wp_id': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['wp_helper']