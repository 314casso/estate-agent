# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from estatebase.models import ProcessDeletedModel, Region, Locality,\
    Street, SimpleDict, Microdistrict, HistoryMeta, Client
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
import datetime
from django.core.validators import RegexValidator

class Address(models.Model):
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.PROTECT) 
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'), on_delete=models.PROTECT, blank=True, null=True)
    microdistrict = models.ForeignKey(Microdistrict, verbose_name=_('Microdistrict'), blank=True, null=True, on_delete=models.PROTECT)
    street = models.ForeignKey(Street, verbose_name=_('Street'), on_delete=models.PROTECT, blank=True, null=True)    
    estate_number = models.CharField(_('Estate number'), max_length=10, blank=True, null=True)    
    def __unicode__(self):
        address_fields = [self.region, self.locality, self.microdistrict, self.street, self.estate_number]
        result = []
        for address_field in address_fields:
            if address_field:          
                result.append(object)             
        return u', '.join(address_field)    
    class Meta:
        ordering = ['id']                

class PartnerType(SimpleDict):
    '''
    PartnerType    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Partner type')
        verbose_name_plural = _('Partner types')

class Quality(SimpleDict):
    '''
    Quality    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Quality')
        verbose_name_plural = _('Qualitys')

class Experience(SimpleDict):
    '''
    Experience    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Experience')
        verbose_name_plural = _('Experiences')

class WorkType(MPTTModel):
    '''
    WorkType    
    '''    
    name = models.CharField(_('Name'), max_length=150, db_index=True, unique=True)
    parent = TreeForeignKey('self', verbose_name=_('Parent'), null=True, blank=True, related_name='children')
    class Meta(SimpleDict.Meta):
        verbose_name = _('Work type')
        verbose_name_plural = _('Work types')
    class MPTTMeta:
        order_insertion_by = ['name']
    def __unicode__(self):
        return u'%s' % (self.name,)

class Measure(SimpleDict):
    '''
    Measure    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Measure')
        verbose_name_plural = _('Measures')

class WorkTypeProfile(models.Model):    
    work_type = models.ForeignKey(WorkType, verbose_name=_('WorkType'))
    dev_profile = models.ForeignKey('DevProfile', verbose_name=_('DevProfile'))
    price_min = models.IntegerField(verbose_name=_('Price min'))
    price_max = models.IntegerField(verbose_name=_('Price max'))
    measure = models.ForeignKey(Measure, verbose_name=_('Measure')) 
    quality = models.ForeignKey(Quality, verbose_name=_('Quality'), blank=True, null=True)
    experience = models.ForeignKey(Experience, verbose_name=_('Experience'), blank=True, null=True)
    class Meta:
        unique_together = ('work_type', 'dev_profile')      

class Gear(SimpleDict):
    '''
    Gear 
    '''
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255)
    class Meta(SimpleDict.Meta):
        verbose_name = _('Gear')
        verbose_name_plural = _('Gears')

class PartnerClientStatus(SimpleDict):
    '''
    PartnerClientStatus    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('PartnerClientStatus')
        verbose_name_plural = _('PartnerClientStatuses')

class ClientPartner(models.Model):    
    client = models.ForeignKey(Client)
    partner = models.ForeignKey('Partner')    
    partner_client_status = models.ForeignKey(PartnerClientStatus, verbose_name=_('PartnerClientStatus'))
    class Meta:
        unique_together = ('client', 'partner')

class DevProfile(models.Model):    
    coverage_regions = models.ManyToManyField(Region, verbose_name=_('Regions'), related_name='person_coverage')
    coverage_localities = models.ManyToManyField(Locality, verbose_name=_('Localities'), related_name='person_coverage')
    quality = models.ForeignKey(Quality, verbose_name=_('Quality'), blank=True, null=True)
    experience = models.ForeignKey(Experience, verbose_name=_('Experience'), blank=True, null=True)
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255)
    work_types = models.ManyToManyField(WorkType, verbose_name=_('WorkTypes'), blank=True, null=True, through=WorkTypeProfile)
    gears = models.ManyToManyField('Gear', verbose_name=_('Gears'), related_name='owners', blank=True, null=True)
    has_transport = models.BooleanField(_('HasTransport'), default=False)    

class ExtraProfile(models.Model):
    GENDER_CHOICES = (('F', _('Female')), ('M', _('Male')),)
    last_name = models.CharField(_('LastName'), max_length=100, blank=True)
    first_name = models.CharField(_('FirstName'), max_length=100, blank=True)
    patronymic = models.CharField(_('Patronymic'), max_length=100, blank=True)
    adress = models.OneToOneField(Address, verbose_name=_('Address'), blank=True, null=True, related_name='extra_profile')
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES, blank=True, default='M')
    birthday = models.DateField(_('Birthday'), default=datetime.date.today(), blank=True)
    birthplace = models.CharField(_('Birthplace'), max_length=250, blank=True)
    passport_number = models.CharField(_('PassportNumber'), max_length=6, blank=True, 
    validators=[
        RegexValidator(regex='^\d{6}$', 
        message=u'Номер паспорта должен состоять из шести цифр', code='invalid_passport_number')
        ]
    )
    passport_series = models.CharField(_('PassportSeries'), max_length=4, blank=True, 
    validators=[
        RegexValidator(regex='^\d{4}$', 
        message='Серия паспорта должена состоять из четырех цифр', code='invalid_passport_series')
        ]
    )

class Partner(ProcessDeletedModel):
    partner_types = models.ManyToManyField(PartnerType, verbose_name=_('Partner types'), related_name='partners')
    dev_profile = models.OneToOneField(DevProfile, verbose_name=_('DevProfile'), blank=True, null=True, related_name='partner') 
    name = models.CharField(_('Name'), max_length=255)
    clients = models.ManyToManyField(Client, verbose_name=_('Clients'), blank=True, null=True, through=ClientPartner)     
    adress = models.OneToOneField(Address, verbose_name=_('Address'), blank=True, null=True, related_name='partner')  
    person_count = models.IntegerField(_('Persons'), default=0)                  
    history = models.OneToOneField(HistoryMeta, blank=True, null=True, editable=False)
    parent = models.ForeignKey('self', verbose_name=_('Parent'), null=True, blank=True, related_name='children')
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255)
    def __unicode__(self):
        return u'%s' % self.name
    def natural_key(self):
        return self.__unicode__()
    class Meta:
        ordering = ['name']
    @models.permalink
    def get_absolute_url(self):
        return ('partner_detail', [str(self.id)])
