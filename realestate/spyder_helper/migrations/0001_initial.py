# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SpyderMeta'
        db.create_table('spyder_helper_spydermeta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('spyder', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=255, db_index=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('spyder_helper', ['SpyderMeta'])


    def backwards(self, orm):
        # Deleting model 'SpyderMeta'
        db.delete_table('spyder_helper_spydermeta')


    models = {
        'spyder_helper.spydermeta': {
            'Meta': {'object_name': 'SpyderMeta'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spyder': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['spyder_helper']