# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WordpressTaxonomyTree'
        db.create_table('wp_helper_wordpresstaxonomytree', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('wp_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['wp_helper.WordpressTaxonomyTree'])),
        ))
        db.send_create_signal('wp_helper', ['WordpressTaxonomyTree'])


    def backwards(self, orm):
        # Deleting model 'WordpressTaxonomyTree'
        db.delete_table('wp_helper_wordpresstaxonomytree')


    models = {
        'wp_helper.wordpresstaxonomytree': {
            'Meta': {'object_name': 'WordpressTaxonomyTree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['wp_helper.WordpressTaxonomyTree']"}),
            'wp_id': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['wp_helper']