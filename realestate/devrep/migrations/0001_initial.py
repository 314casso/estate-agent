# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Address'
        db.create_table('devrep_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Region'], on_delete=models.PROTECT)),
            ('locality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Locality'], null=True, on_delete=models.PROTECT, blank=True)),
            ('microdistrict', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Microdistrict'], null=True, on_delete=models.PROTECT, blank=True)),
            ('street', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estatebase.Street'], null=True, on_delete=models.PROTECT, blank=True)),
            ('estate_number', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal('devrep', ['Address'])

        # Adding model 'Contact'
        db.create_table('devrep_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('contact_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person_contacts', on_delete=models.PROTECT, to=orm['estatebase.ContactType'])),
            ('contact', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal('devrep', ['Contact'])

        # Adding model 'PartnerType'
        db.create_table('devrep_partnertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal('devrep', ['PartnerType'])

        # Adding model 'Quality'
        db.create_table('devrep_quality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal('devrep', ['Quality'])

        # Adding model 'Experience'
        db.create_table('devrep_experience', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal('devrep', ['Experience'])

        # Adding model 'WorkType'
        db.create_table('devrep_worktype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['devrep.WorkType'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('devrep', ['WorkType'])

        # Adding model 'Measure'
        db.create_table('devrep_measure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal('devrep', ['Measure'])

        # Adding model 'WorkTypePartner'
        db.create_table('devrep_worktypepartner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('work_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['devrep.WorkType'])),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['devrep.Partner'])),
            ('price_min', self.gf('django.db.models.fields.IntegerField')()),
            ('price_max', self.gf('django.db.models.fields.IntegerField')()),
            ('measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['devrep.Measure'])),
            ('quality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['devrep.Quality'], null=True, blank=True)),
            ('experience', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['devrep.Experience'], null=True, blank=True)),
        ))
        db.send_create_signal('devrep', ['WorkTypePartner'])

        # Adding unique constraint on 'WorkTypePartner', fields ['work_type', 'partner']
        db.create_unique('devrep_worktypepartner', ['work_type_id', 'partner_id'])

        # Adding model 'Gear'
        db.create_table('devrep_gear', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('devrep', ['Gear'])

        # Adding model 'Partner'
        db.create_table('devrep_partner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('adress', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['devrep.Address'], on_delete=models.PROTECT)),
            ('person_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('quality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['devrep.Quality'], null=True, blank=True)),
            ('experience', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['devrep.Experience'], null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('devrep', ['Partner'])

        # Adding M2M table for field partner_types on 'Partner'
        m2m_table_name = db.shorten_name('devrep_partner_partner_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['devrep.partner'], null=False)),
            ('partnertype', models.ForeignKey(orm['devrep.partnertype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partner_id', 'partnertype_id'])

        # Adding M2M table for field contacts on 'Partner'
        m2m_table_name = db.shorten_name('devrep_partner_contacts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['devrep.partner'], null=False)),
            ('contact', models.ForeignKey(orm['devrep.contact'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partner_id', 'contact_id'])

        # Adding M2M table for field coverage_regions on 'Partner'
        m2m_table_name = db.shorten_name('devrep_partner_coverage_regions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['devrep.partner'], null=False)),
            ('region', models.ForeignKey(orm['estatebase.region'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partner_id', 'region_id'])

        # Adding M2M table for field coverage_localities on 'Partner'
        m2m_table_name = db.shorten_name('devrep_partner_coverage_localities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['devrep.partner'], null=False)),
            ('locality', models.ForeignKey(orm['estatebase.locality'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partner_id', 'locality_id'])

        # Adding M2M table for field gears on 'Partner'
        m2m_table_name = db.shorten_name('devrep_partner_gears')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['devrep.partner'], null=False)),
            ('gear', models.ForeignKey(orm['devrep.gear'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partner_id', 'gear_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'WorkTypePartner', fields ['work_type', 'partner']
        db.delete_unique('devrep_worktypepartner', ['work_type_id', 'partner_id'])

        # Deleting model 'Address'
        db.delete_table('devrep_address')

        # Deleting model 'Contact'
        db.delete_table('devrep_contact')

        # Deleting model 'PartnerType'
        db.delete_table('devrep_partnertype')

        # Deleting model 'Quality'
        db.delete_table('devrep_quality')

        # Deleting model 'Experience'
        db.delete_table('devrep_experience')

        # Deleting model 'WorkType'
        db.delete_table('devrep_worktype')

        # Deleting model 'Measure'
        db.delete_table('devrep_measure')

        # Deleting model 'WorkTypePartner'
        db.delete_table('devrep_worktypepartner')

        # Deleting model 'Gear'
        db.delete_table('devrep_gear')

        # Deleting model 'Partner'
        db.delete_table('devrep_partner')

        # Removing M2M table for field partner_types on 'Partner'
        db.delete_table(db.shorten_name('devrep_partner_partner_types'))

        # Removing M2M table for field contacts on 'Partner'
        db.delete_table(db.shorten_name('devrep_partner_contacts'))

        # Removing M2M table for field coverage_regions on 'Partner'
        db.delete_table(db.shorten_name('devrep_partner_coverage_regions'))

        # Removing M2M table for field coverage_localities on 'Partner'
        db.delete_table(db.shorten_name('devrep_partner_coverage_localities'))

        # Removing M2M table for field gears on 'Partner'
        db.delete_table(db.shorten_name('devrep_partner_gears'))


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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
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