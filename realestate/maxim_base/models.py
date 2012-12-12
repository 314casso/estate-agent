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
    
#    @property
#    def i_creator_id(self):
#        if self.creator_id:
#            return UserUser.objects.get(pk=self.creator_id).user_id
#
    @property
    def i_source_id(self):
        origin_mapper = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 10, 8: 14, 9: 7, 10: 8, 11: 9, 12: 11, 13: 13, 14: 12}
        if self.source_id in origin_mapper:
            return origin_mapper[self.source_id]        
#    
#    @property
#    def i_last_editor_id(self):
#        if self.last_editor_id:
#            return UserUser.objects.get(pk=self.last_editor_id).user_id
                        
    def __unicode__(self):
        return u'%s (%s)' % (self.pk, self.status_id)
    class Meta:
        db_table = u'real_estate'
        managed = False                      
                                