# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SourceOrigin'
        db.delete_table('migrate_app_sourceorigin')


    def backwards(self, orm):
        # Adding model 'SourceOrigin'
        db.create_table('migrate_app_sourceorigin', (
            ('origin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Origin'])),
            ('source_id', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('migrate_app', ['SourceOrigin'])


    models = {
        
    }

    complete_apps = ['migrate_app']