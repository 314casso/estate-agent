# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'SpiderMeta', fields ['spider']
        db.delete_unique('spyder_helper_spidermeta', ['spider'])

        # Adding index on 'SpiderMeta', fields ['status']
        db.create_index('spyder_helper_spidermeta', ['status'])

        # Adding index on 'SpiderMeta', fields ['spider']
        db.create_index('spyder_helper_spidermeta', ['spider'])


    def backwards(self, orm):
        # Removing index on 'SpiderMeta', fields ['spider']
        db.delete_index('spyder_helper_spidermeta', ['spider'])

        # Removing index on 'SpiderMeta', fields ['status']
        db.delete_index('spyder_helper_spidermeta', ['status'])

        # Adding unique constraint on 'SpiderMeta', fields ['spider']
        db.create_unique('spyder_helper_spidermeta', ['spider'])


    models = {
        'spyder_helper.spidermeta': {
            'Meta': {'object_name': 'SpiderMeta'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spider': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['spyder_helper']