# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from orderedmodel.models import OrderedModel
import datetime
from django.contrib.auth.models import User

class ExUser(User):
    def __unicode__(self):
        return u'%s %s (%s)' % (self.first_name, self.last_name, self.username)
    class Meta:
        proxy = True    

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

OBJECT_TYPE_CHOICES = (
    ('BIDG', 'Строение'),
    ('STEAD', 'Участок'),
)

class EstateType(OrderedModel):
    name = models.CharField(_('Name'), max_length=100)
    estate_type_category = models.ForeignKey(EstateTypeCategory, verbose_name=_('EstateTypeCategory'),)    
    object_type = models.CharField(_('Object type'), max_length=50, choices=OBJECT_TYPE_CHOICES)
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255)
    @property
    def reverse_link(self):
        reverse_links = {
                         'BIDG':'bidg_create',
                         'STEAD':'bidg_create',
                         }
        return reverse_links[self.object_type]

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

class Bidg(Estate):    
    room_number = models.CharField(_('Room number'), max_length=10)
    class Meta:
        verbose_name = _('bidg')
        verbose_name_plural = _('bidgs')

class ClientType(SimpleDict):    
    class Meta(SimpleDict.Meta):
        verbose_name = _('client type')
        verbose_name_plural = _('client types')

class Origin(SimpleDict):
    class Meta(SimpleDict.Meta):
        verbose_name = _('origin')
        verbose_name_plural = _('origins')

class Client(models.Model):
    """
    An client entity      
    """
    name = models.CharField(_('Name'), max_length=255)
    client_type = models.ForeignKey(ClientType, verbose_name=_('ClientType'),)
    origin = models.ForeignKey(Origin, verbose_name=_('Origin'), blank=True, null=True) 
    address = models.CharField(_('Address'), blank=True, null=True, max_length=255)
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255)
    created_by = models.ForeignKey(ExUser, verbose_name=_('User'), blank=True, null=True, related_name='creators')
    created = models.DateTimeField(_('Created'), blank=True, null=True)
    updated = models.DateTimeField(_('Updated'), blank=True, null=True)
    updated_by = models.ForeignKey(ExUser, verbose_name=_('Updated by'), blank=True, null=True, related_name='updaters')     
    def __unicode__(self):
        return u'%s %s' % (self.name, self.address)
    @property
    def contacts(self):
        return self.contactlist.all().select_related('contact_type')
    @property
    def user(self):
        return self.updated_by or self.created_by 
    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)                                           
        if not self.id:
            self.created = datetime.datetime.now()
            self.created_by = user
        else:    
            self.updated = datetime.datetime.now()
            self.updated_by = user                                     
        super(Client, self).save(*args, **kwargs)    
    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')
        ordering = ['id']    

class ContactType(SimpleDict):
    class Meta(SimpleDict.Meta):
        verbose_name = _('contact type')
        verbose_name_plural = _('contact types')

class ContactState(SimpleDict):
    class Meta(SimpleDict.Meta):
        verbose_name = _('contact state')
        verbose_name_plural = _('contact states')

class ContactHistory(models.Model):
    event_date = models.DateTimeField(_('Event Date'), default=datetime.datetime.now())
    user = models.ForeignKey(ExUser, verbose_name=_('User'), blank=True, null=True)
    contact_state = models.ForeignKey(ContactState, verbose_name=_('Contact State'),) 
    contact = models.ForeignKey('Contact', verbose_name=_('Contact'),)
    def __unicode__(self):
        return u'%s: %s' % (self.event_date, self.contact_state.name)
    class Meta:
        verbose_name = _('contact history')
        verbose_name_plural = _('contact history') 

class Contact(models.Model):    
    client = models.ForeignKey(Client, verbose_name=_('Client'), related_name='contactlist')
    contact_type = models.ForeignKey(ContactType, verbose_name=_('ContactType'),)
    contact = models.CharField(_('Contact'), max_length=255, db_index=True)
    updated = models.DateTimeField(_('Created'), blank=True, null=True)   
    contact_state = models.ForeignKey(ContactState, verbose_name=_('Contact State'), default=5)     
    def __unicode__(self):
        return u'%s: %s' % (self.contact_type.name, self.contact)
    @property
    def state_css(self):
        css = {1:'available-state', 2:'non-available-state', 3:'ban-state', 4:'not-responded-state', 5:'not-checked-state'}                             
        return self.contact_state.pk in css and css[self.contact_state.pk] or ''                
    def clean(self):
        from django.core.validators import validate_email
        from django.core.validators import URLValidator
        from django.core.validators import RegexValidator          
        validate_url = URLValidator(verify_exists=False)
        validate_phone = RegexValidator(regex=r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')        
        if self.contact_type.id == 1:
            validate_phone(self.contact)
        elif self.contact_type.id == 2:
            validate_email(self.contact)
        elif self.contact_type.id == 3:
            validate_url(self.contact)
    def save(self, *args, **kwargs):
        '''
        TODO:Нужно продумать логику обновления клиента
        '''
        self.updated = datetime.datetime.now()     
        super(Contact, self).save(*args, **kwargs)                      
        try: 
            latest = self.contacthistory_set.latest('event_date')
        except ContactHistory.DoesNotExist:
            latest = None    
        if latest:                        
            if (latest.contact_state == self.contact_state) and (latest.event_date > self.updated - datetime.timedelta(minutes=20)):
                return             
        contact_history = ContactHistory(event_date=self.updated, 
                                         contact_state=self.contact_state, contact=self, 
                                         user_id=Client.objects.get(pk=self.client_id).user.pk)
        contact_history.save()                                            
    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts') 
        ordering = ['contact_type__pk']  


    
