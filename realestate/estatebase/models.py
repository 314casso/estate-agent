# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from orderedmodel.models import OrderedModel

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


# Client Object Model
class ClientType(SimpleDict):
    class Meta(SimpleDict.Meta):
        verbose_name = _('client type')
        verbose_name_plural = _('client types')

class Origin(SimpleDict):
    class Meta(SimpleDict.Meta):
        verbose_name = _('origin')
        verbose_name_plural = _('origins')

class Client(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    client_type = models.ForeignKey(ClientType, verbose_name=_('ClientType'),)
    origin = models.ForeignKey(Origin, verbose_name=_('Origin'), blank=True, null=True) # Source where this contact was found
    address = models.CharField(_('Address'), blank=True, null=True, max_length=255)
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255)
    def __unicode__(self):
        return u'%s %s' % (self.name, self.address)
    @property
    def contacts(self):
        return self.contact_set.all().select_related('contact_type')
    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')
        ordering = ['id']    

class ContactType(SimpleDict):
    class Meta(SimpleDict.Meta):
        verbose_name = _('contact type')
        verbose_name_plural = _('contact types')

class Contact(models.Model):
    client = models.ForeignKey(Client, verbose_name=_('Client'),)
    contact_type = models.ForeignKey(ContactType, verbose_name=_('ContactType'),)
    contact = models.CharField(_('Contact'), max_length=255)        
    def __unicode__(self):
        return u'%s: %s' % (self.contact_type.name, self.contact)
    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts') 
        ordering = ['contact_type__pk']  

class ContactState(SimpleDict):
    class Meta(SimpleDict.Meta):
        verbose_name = _('contact state')
        verbose_name_plural = _('contact states')

class ContactHistory(models.Model):
    event_date = models.DateTimeField(_('Event Date'))
    contact_state = models.ForeignKey(ContactState, verbose_name=_('Contact State'),) 
    def __unicode__(self):
        return u'%s: %s' % (self.event_date, self.contact_state.name)
    class Meta:
        verbose_name = _('contact history')
        verbose_name_plural = _('contact history') 
    
