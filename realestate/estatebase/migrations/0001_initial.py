# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Estate'
        db.create_table('estatebase_estate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('estatebase', ['Estate'])

        # Adding model 'Region'
        db.create_table('estatebase_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('estatebase', ['Region'])

        # Adding model 'Locality'
        db.create_table('estatebase_locality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Region'], null=True, blank=True)),
        ))
        db.send_create_signal('estatebase', ['Locality'])

        # Adding model 'Microdistrict'
        db.create_table('estatebase_microdistrict', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('locality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Locality'])),
        ))
        db.send_create_signal('estatebase', ['Microdistrict'])

        # Adding model 'Street'
        db.create_table('estatebase_street', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('locality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Locality'])),
        ))
        db.send_create_signal('estatebase', ['Street'])


    def backwards(self, orm):
        
        # Deleting model 'Estate'
        db.delete_table('estatebase_estate')

        # Deleting model 'Region'
        db.delete_table('estatebase_region')

        # Deleting model 'Locality'
        db.delete_table('estatebase_locality')

        # Deleting model 'Microdistrict'
        db.delete_table('estatebase_microdistrict')

        # Deleting model 'Street'
        db.delete_table('estatebase_street')


    models = {
        'estatebase.estate': {
            'Meta': {'object_name': 'Estate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'estatebase.locality': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Locality'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Region']", 'null': 'True', 'blank': 'True'})
        },
        'estatebase.microdistrict': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Microdistrict'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.region': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'estatebase.street': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Street'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['estatebase']
