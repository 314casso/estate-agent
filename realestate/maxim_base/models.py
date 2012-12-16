# -*- coding: utf-8 -*-
from django.db import models

class Source(models.Model):
    name = models.CharField('Name', max_length=50)    
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        db_table = u'source'
        managed = False
    
class Customers(models.Model):
    creator_id = models.IntegerField()
    source = models.ForeignKey(Source)
    treatment_date = models.DateTimeField()
    name = models.CharField(max_length=90)
    comments = models.CharField(max_length=765, blank=True)
    from_where = models.CharField(max_length=765, blank=True)
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        db_table = u'customers'
        managed = False
        
class Contacts(models.Model):
    customer = models.ForeignKey(Customers, related_name='contacts')
    contact = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=36, blank=True)
    update_record = models.DateTimeField()
    def __unicode__(self):
        return u'%s' % self.contact
    class Meta:
        db_table = u'contacts'
        managed = False

class Users(models.Model):
    user = models.CharField(max_length=48)
    name = models.CharField(max_length=75)
    last_logon = models.DateTimeField(null=True, blank=True)
    def __unicode__(self):
        return u'%s (%s)' % (self.name,self.user)
    class Meta:
        db_table = u'users'
        managed = False
                        
class Types(models.Model):
    name = models.CharField(max_length=90, unique=True)
    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        db_table = u'types'
        managed = False
        ordering = ['name']

class Region(models.Model):
    name = models.CharField(max_length=90, unique=True)
    class Meta:
        db_table = u'region'
        managed = False

class Place(models.Model):
    name = models.CharField(max_length=75, unique=True)
    class Meta:
        db_table = u'place'
        managed = False

class Street(models.Model):
    name = models.CharField(max_length=75, unique=True)
    class Meta:
        db_table = u'street'
        managed = False

class Area(models.Model):
    name = models.CharField(max_length=300, unique=True)
    class Meta:
        db_table = u'area'
        managed = False                        
                       
class RealEstate(models.Model):
    type_id = models.IntegerField()
    creator_id = models.IntegerField()
    source_id = models.IntegerField()
    creation_date = models.DateTimeField()
    last_editor_id = models.IntegerField(null=True, blank=True)
    update_record = models.DateTimeField()
    region = models.ForeignKey(Region, null=True, blank=True)
    place = models.ForeignKey(Place, null=True, blank=True)
    street = models.ForeignKey(Street, null=True, blank=True)
    house_number = models.CharField(max_length=15, blank=True)
    area = models.ForeignKey(Area, null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    cost_markup = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=42)
    @property
    def status_id(self):
        if self.status:
            dest_map = {
            u'вакантно': 1,
            u'новая': 2,
            u'продано': 3,
            u'снят с продажи': 4,
            }
            return dest_map[self.status]
    def __unicode__(self):
        return u'%s (%s)' % (self.pk, self.status_id)
    class Meta:
        db_table = u'real_estate'
        managed = False                    
    
class CustomerHasRealEstate(models.Model):
    real_estate = models.ForeignKey(RealEstate, unique=True, related_name='customers')
    customer = models.ForeignKey(Customers)
    class Meta:
        db_table = u'customer_has_real_estate'
        managed = False

class Images(models.Model):    
    real_estate = models.ForeignKey(RealEstate, related_name='images')
    file_name = models.CharField(max_length=96)
    class Meta:
        db_table = u'images'
        managed = False     

class Properties(models.Model):
    real_estate = models.ForeignKey(RealEstate, unique=True)
    name = models.CharField(max_length=75, unique=True)
    value = models.CharField(max_length=765)
    class Meta:
        db_table = u'properties'
        managed = False

class Descriptions(models.Model):
    real_estate = models.ForeignKey(RealEstate, unique=True)
    description = models.TextField()
    def __unicode__(self):
        return u'%s' % self.description.strip()
    class Meta:
        db_table = u'descriptions'
        managed = False                                                       