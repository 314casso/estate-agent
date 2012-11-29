# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SourceOrigin'
        db.create_table('migrate_app_sourceorigin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('origin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Origin'])),
            ('source_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('migrate_app', ['SourceOrigin'])


    def backwards(self, orm):
        # Deleting model 'SourceOrigin'
        db.delete_table('migrate_app_sourceorigin')


    models = {
        'estatebase.origin': {
            'Meta': {'ordering': "['name']", 'object_name': 'Origin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'migrate_app.sourceorigin': {
            'Meta': {'object_name': 'SourceOrigin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Origin']"}),
            'source_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['migrate_app']