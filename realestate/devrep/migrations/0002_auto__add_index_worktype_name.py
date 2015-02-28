# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'WorkType', fields ['name']
        db.create_index('devrep_worktype', ['name'])


    def backwards(self, orm):
        # Removing index on 'WorkType', fields ['name']
        db.delete_index('devrep_worktype', ['name'])


    models = {
        'devrep.address': {
            'Meta': {'ordering': "['id']", 'object_name': 'Address'},
            'estate_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'microdistrict': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Microdistrict']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Region']", 'on_delete': 'models.PROTECT'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Street']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'})
        },
        'devrep.contact': {
            'Meta': {'object_name': 'Contact'},
            'contact': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_contacts'", 'on_delete': 'models.PROTECT', 'to': "orm['estatebase.ContactType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'devrep.experience': {
            'Meta': {'ordering': "['name']", 'object_name': 'Experience'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'devrep.gear': {
            'Meta': {'ordering': "['name']", 'object_name': 'Gear'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'devrep.measure': {
            'Meta': {'ordering': "['name']", 'object_name': 'Measure'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'devrep.partner': {
            'Meta': {'object_name': 'Partner'},
            'adress': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['devrep.Address']", 'on_delete': 'models.PROTECT'}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'person_contacts'", 'symmetrical': 'False', 'to': "orm['devrep.Contact']"}),
            'coverage_localities': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'person_coverage'", 'symmetrical': 'False', 'to': "orm['estatebase.Locality']"}),
            'coverage_regions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'person_coverage'", 'symmetrical': 'False', 'to': "orm['estatebase.Region']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'experience': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['devrep.Experience']", 'null': 'True', 'blank': 'True'}),
            'gears': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'owners'", 'symmetrical': 'False', 'to': "orm['devrep.Gear']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'partner_types': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'partners'", 'symmetrical': 'False', 'to': "orm['devrep.PartnerType']"}),
            'person_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['devrep.Quality']", 'null': 'True', 'blank': 'True'}),
            'work_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['devrep.WorkType']", 'null': 'True', 'through': "orm['devrep.WorkTypePartner']", 'blank': 'True'})
        },
        'devrep.partnertype': {
            'Meta': {'ordering': "['name']", 'object_name': 'PartnerType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'devrep.quality': {
            'Meta': {'ordering': "['name']", 'object_name': 'Quality'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'devrep.worktype': {
            'Meta': {'ordering': "['name']", 'object_name': 'WorkType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['devrep.WorkType']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'devrep.worktypepartner': {
            'Meta': {'unique_together': "(('work_type', 'partner'),)", 'object_name': 'WorkTypePartner'},
            'experience': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['devrep.Experience']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['devrep.Measure']"}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['devrep.Partner']"}),
            'price_max': ('django.db.models.fields.IntegerField', [], {}),
            'price_min': ('django.db.models.fields.IntegerField', [], {}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['devrep.Quality']", 'null': 'True', 'blank': 'True'}),
            'work_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['devrep.WorkType']"})
        },
        'estatebase.contacttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ContactType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
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
            'name_gent': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_loct': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Region']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'})
        },
        'estatebase.localitytype': {
            'Meta': {'ordering': "['name']", 'object_name': 'LocalityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'prep_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'sort_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'estatebase.microdistrict': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'locality'),)", 'object_name': 'Microdistrict'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']", 'on_delete': 'models.PROTECT'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'estatebase.region': {
            'Meta': {'ordering': "['name']", 'object_name': 'Region'},
            'geo_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.GeoGroup']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metropolis': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'metropolis_region'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['estatebase.Locality']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'regular_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'regular_name_gent': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'estatebase.street': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'locality', 'street_type'),)", 'object_name': 'Street'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.Locality']", 'on_delete': 'models.PROTECT'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'street_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['estatebase.StreetType']", 'on_delete': 'models.PROTECT'})
        },
        'estatebase.streettype': {
            'Meta': {'ordering': "['name']", 'object_name': 'StreetType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['devrep']