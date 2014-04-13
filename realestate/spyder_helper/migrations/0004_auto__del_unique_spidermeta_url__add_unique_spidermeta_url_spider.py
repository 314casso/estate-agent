# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'SpiderMeta', fields ['url']
        db.delete_unique('spyder_helper_spidermeta', ['url'])

        # Adding unique constraint on 'SpiderMeta', fields ['url', 'spider']
        db.create_unique('spyder_helper_spidermeta', ['url', 'spider'])


    def backwards(self, orm):
        # Removing unique constraint on 'SpiderMeta', fields ['url', 'spider']
        db.delete_unique('spyder_helper_spidermeta', ['url', 'spider'])

        # Adding unique constraint on 'SpiderMeta', fields ['url']
        db.create_unique('spyder_helper_spidermeta', ['url'])


    models = {
        'spyder_helper.spidermeta': {
            'Meta': {'unique_together': "(('spider', 'url'),)", 'object_name': 'SpiderMeta'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spider': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['spyder_helper']