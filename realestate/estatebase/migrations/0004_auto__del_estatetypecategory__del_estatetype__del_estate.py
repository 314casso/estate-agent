# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'EstateTypeCategory'
        db.delete_table('estatebase_estatetypecategory')

        # Deleting model 'EstateType'
        db.delete_table('estatebase_estatetype')

        # Deleting model 'Estate'
        db.delete_table('estatebase_estate')


    def backwards(self, orm):
        
        # Adding model 'EstateTypeCategory'
        db.create_table('estatebase_estatetypecategory', (
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('estatebase', ['EstateTypeCategory'])

        # Adding model 'EstateType'
        db.create_table('estatebase_estatetype', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('estate_type_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.EstateTypeCategory'])),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('estatebase', ['EstateType'])

        # Adding model 'Estate'
        db.create_table('estatebase_estate', (
            ('estate_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.EstateType'], null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('estatebase', ['Estate'])


    models = {
        'estatebase.locality': {
            'Meta': {'ordering': "['name']", 'object_name': 'Locality'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Region']", 'null': 'True', 'blank': 'True'})
        },
        'estatebase.microdistrict': {
            'Meta': {'ordering': "['name']", 'object_name': 'Microdistrict'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.region': {
            'Meta': {'ordering': "['name']", 'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.street': {
            'Meta': {'ordering': "['name']", 'object_name': 'Street'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['estatebase']
