# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from realestate.orderedmodel.models import OrderedModel

class SimpleDict(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        ordering = ['name']
        abstract = True

class Region(SimpleDict):
    class Meta(SimpleDict.Meta):
        verbose_name = _('region')
        verbose_name_plural = _('regions')

class Locality(SimpleDict):
    region = models.ForeignKey(Region, blank=True, null=True, verbose_name=_('Region'),)
    class Meta(SimpleDict.Meta):
        verbose_name = _('locality')
        verbose_name_plural = _('localities')    

class Microdistrict(SimpleDict):
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'),)
    class Meta(SimpleDict.Meta):
        verbose_name = _('microdistrict')
        verbose_name_plural = _('microdistricts')

class Street(SimpleDict):
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'),)
    class Meta(SimpleDict.Meta):
        verbose_name = _('street')
        verbose_name_plural = _('streets')

class EstateTypeCategory(OrderedModel):
    name = models.CharField(_('Name'), max_length=100)
    def __unicode__(self):
        return u'%s' % self.name
    class Meta(OrderedModel.Meta):
        verbose_name = _('estate type category')
        verbose_name_plural = _('estate type categories')        

class EstateType(OrderedModel):
    name = models.CharField(_('Name'), max_length=100)
    estate_type_category = models.ForeignKey(EstateTypeCategory, verbose_name=_('EstateTypeCategory'),)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name=_('ContentType'), limit_choices_to={'id__in': [3, 11]})
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255)
    def __unicode__(self):
        return u'%s' % self.name    
    class Meta(OrderedModel.Meta):
        verbose_name = _('estate type')
        verbose_name_plural = _('estate types')     
    
class Estate(models.Model):
    estate_type = models.ForeignKey(EstateType, blank=True, null=True, verbose_name=_('EstateType'),)
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'),)
    street = models.ForeignKey(Street, verbose_name=_('Street'),)    
    class Meta:
        verbose_name = _('estate')
        verbose_name_plural = _('estate')

#class Bidg(Estate):    
#    class Meta:
#        verbose_name = _('bidg')
#        verbose_name_plural = _('bidgs')
            
