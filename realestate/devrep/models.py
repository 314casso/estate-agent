# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from estatebase.models import ProcessDeletedModel, Region, Locality,\
     SimpleDict, HistoryMeta, Client, AVAILABILITY_CHOICES
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.core.validators import RegexValidator


class Address(models.Model):
    region = models.CharField(_('Region'), max_length=100, blank=True, null=True)
    locality = models.CharField(_('Locality'), max_length=100, blank=True, null=True)  
    address = models.CharField(_('ExtraAddress'), max_length=150, blank=True, null=True)    
    
    def __unicode__(self):
        address_fields = [self.region, self.locality, self.address]
        result = []
        for address_field in address_fields:            
            if address_field:          
                result.append(u'%s' % address_field)
        return u', '.join(result)    
    
    class Meta:
        ordering = ['id']                


class PartnerType(SimpleDict):
    '''
    PartnerType    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Partner type')
        verbose_name_plural = _('Partner types')


class Citizenship(SimpleDict):
    '''
    Citizenship    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Citizenship')
        verbose_name_plural = _('Citizenships')


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


class Goods(MPTTModel):
    '''
    Goods and Service    
    '''
    TYPE_CHOICES = (('G', _('Goods')), ('S', _('Service')),)
    name = models.CharField(_('Name'), max_length=150, db_index=True, unique=True)
    parent = TreeForeignKey('self', verbose_name=_('Parent'), null=True, blank=True, related_name='children')
    type = models.CharField(_('Type'), max_length=1, choices=TYPE_CHOICES, blank=True, default='G', db_index=True)
    measure = models.ForeignKey('Measure', verbose_name=_('Measure'), blank=True, null=True)
    
    class Meta(SimpleDict.Meta):
        verbose_name = _('GoodsService')
        verbose_name_plural = _('GoodsServices')
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    def __unicode__(self):
        return u'%s' % (self.name,)


class GoodsProfileM2M(models.Model):
    goods = models.ForeignKey(Goods, verbose_name=_('Goods'))
    dev_profile = models.ForeignKey('DevProfile', verbose_name=_('DevProfile'))
    price = models.IntegerField(verbose_name=_('Price min'), blank=True, null=True)    
    measure = models.ForeignKey('Measure', verbose_name=_('Measure'), blank=True, null=True)
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255)
    
    class Meta:
        unique_together = ('goods', 'dev_profile')    


class WorkType(MPTTModel):
    '''
    WorkType    
    '''    
    name = models.CharField(_('Name'), max_length=150, db_index=True, unique=True)
    parent = TreeForeignKey('self', verbose_name=_('Parent'), null=True, blank=True, related_name='children')
    measure = models.ForeignKey('Measure', verbose_name=_('Measure'), blank=True, null=True)
    
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
    price_min = models.IntegerField(verbose_name=_('Price min'), blank=True, null=True)
    price_max = models.IntegerField(verbose_name=_('Price max'), blank=True, null=True)
    measure = models.ForeignKey(Measure, verbose_name=_('Measure'), blank=True, null=True) 
    quality = models.ForeignKey(Quality, verbose_name=_('Quality'), blank=True, null=True)
    experience = models.ForeignKey(Experience, verbose_name=_('Experience'), blank=True, null=True)
    note = models.TextField(_('Note'), blank=True, null=True)
    
    class Meta:
        unique_together = ('work_type', 'dev_profile')  
        verbose_name = _('WorkTypeProfile')
        verbose_name_plural = _('WorkTypeProfiles')    


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
    coverage_regions = models.ManyToManyField(Region, verbose_name=_('Regions'), related_name='person_coverage', blank=True, null=True)
    coverage_localities = models.ManyToManyField(Locality, verbose_name=_('Localities'), related_name='person_coverage', blank=True, null=True)
    quality = models.ForeignKey(Quality, verbose_name=_('Quality'), blank=True, null=True)
    experience = models.ForeignKey(Experience, verbose_name=_('Experience'), blank=True, null=True)
    note = models.TextField(_('Note'), blank=True, null=True)
    work_types = models.ManyToManyField(WorkType, verbose_name=_('WorkTypes'), blank=True, null=True, through=WorkTypeProfile)
    goods = models.ManyToManyField(Goods, verbose_name=_('Goods'), blank=True, null=True, through=GoodsProfileM2M)
    gears = models.IntegerField(_('Gears'), choices=AVAILABILITY_CHOICES, blank=True, null=True)
    transport = models.IntegerField(_('HasTransport'), choices=AVAILABILITY_CHOICES, blank=True, null=True)
    history = models.OneToOneField(HistoryMeta, blank=True, null=True, editable=False)
    bad_habits = models.CharField(_('BadHabits'), max_length=100, blank=True, null=True) # Вредные привычки 
    progress = models.CharField(_('Progress'), max_length=200, blank=True, null=True) # Достижения
    pc_skills = models.CharField(_('PCSkills'), max_length=100, blank=True, null=True) # Уровень пользователя ПК
    
    class Meta:
        permissions = (
                ("developer", u'Просмотр информации по строительству'),
            )
    
    def __unicode__(self):
        return u'%s' % self.id
    
    def natural_key(self):
        return self.__unicode__()
    
    def get_coverage_regions(self):
        return ', '.join([str(item) for item in self.coverage_regions.all()])          
    
    def get_coverage_localities(self):
        return ', '.join([str(item) for item in self.coverage_localities.all()])
                

class ExtraProfile(models.Model):
    GENDER_CHOICES = (('F', _('Female')), ('M', _('Male')),)
    last_name = models.CharField(_('LastName'), max_length=100,) # Фамилия
    first_name = models.CharField(_('FirstName'), max_length=100,) # Имя
    patronymic = models.CharField(_('Patronymic'), max_length=100, blank=True) # Отчество
    address = models.OneToOneField(Address, verbose_name=_('Address'), blank=True, null=True, related_name='extra_profile')
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES, default='M')
    birthday = models.DateField(_('Birthday'), blank=True, null=True)
    birthplace = models.CharField(_('Birthplace'), max_length=250, blank=True, null=True)
    passport_number = models.CharField(_('PassportNumber'), max_length=6, blank=True, null=True,
    validators=[
        RegexValidator(regex='^\d{6}$', 
        message=u'Номер паспорта должен состоять из шести цифр', code='invalid_passport_number')
        ]
    )
    passport_series = models.CharField(_('PassportSeries'), max_length=4, blank=True, null=True,
    validators=[
        RegexValidator(regex='^\d{4}$', 
        message='Серия паспорта должена состоять из четырех цифр', code='invalid_passport_series')
        ]
    )
    citizenship = models.ForeignKey(Citizenship, verbose_name=_('Citizenship'), null=True, blank=True) # Гражданство

    def __unicode__(self):
        return u'%s %s %s' % (self.last_name, self.first_name, self.patronymic) 


class Partner(ProcessDeletedModel):
    partner_type = models.ForeignKey(PartnerType, verbose_name=_('Partner type'), related_name='partner')     
    name = models.CharField(_('Name'), max_length=255)
    clients = models.ManyToManyField(Client, verbose_name=_('Clients'), blank=True, null=True, through=ClientPartner)     
    address = models.OneToOneField(Address, verbose_name=_('Address'), blank=True, null=True, related_name='partner')  
    person_count = models.IntegerField(_('Persons'), default=0)                  
    history = models.OneToOneField(HistoryMeta, blank=True, null=True, editable=False)
    parent = models.ForeignKey('self', verbose_name=_('Parent'), null=True, blank=True, related_name='children')
    note = models.CharField(_('Note'), blank=True, null=True, max_length=1000)
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def natural_key(self):
        return self.__unicode__()
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')
    
    @models.permalink
    def get_absolute_url(self):
        return ('partner_detail', [str(self.id)])
    
    def get_staff(self):
        return ', '.join([item.name for item in self.clients.all()])
    
