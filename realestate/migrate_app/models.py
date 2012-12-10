from django.db import models
from estatebase.models import Origin, EstateType
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
        