from django.db import models
from estatebase.models import Origin, EstateType, Bid, Estate
from maxim_base.models import Source, Users, Types
from django.contrib.auth.models import User

class SourceOrigin(models.Model):
    origin = models.ForeignKey(Origin)
    source_id = models.IntegerField(primary_key=True)
    @property
    def source(self):        
        return Source.objects.get(pk=self.source_id)
    def __unicode__(self):
        return u'%s, %s'  % (self.origin, self.source)

class UserUser(models.Model):
    user = models.ForeignKey(User, null=True)
    source_id = models.IntegerField(primary_key=True)
    @property
    def source(self):        
        return Users.objects.get(pk=self.source_id)
    def __unicode__(self):
        return u'%s, %s'  % (self.user, self.source)

class TypesEstateType(models.Model):
    estate_type = models.ForeignKey(EstateType, null=True)
    source_id = models.IntegerField(primary_key=True)
    @property
    def source(self):        
        return Types.objects.get(pk=self.source_id)
    def __unicode__(self):
        return u'%s, %s'  % (self.estate_type, self.source)

class BidImport(models.Model):
    bid = models.ForeignKey(Bid)
    external_id = models.IntegerField(unique=True)

class EstateImport(models.Model):
    estate = models.ForeignKey(Estate, blank=True, null=True, on_delete=models.SET_NULL)
    external_id = models.IntegerField(unique=True)
    def __unicode__(self):
        return u'%s'  % self.estate
        