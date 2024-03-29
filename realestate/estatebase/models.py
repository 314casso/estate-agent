# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator, RegexValidator, validate_email
from django.db import models
from django.db.models.aggregates import Sum
from django.utils.translation import ugettext_lazy as _
from orderedmodel.models import OrderedModel
from sorl.thumbnail.fields import ImageField
import datetime
import os
from picklefield.fields import PickledObjectField
from settings import INTEREST_RATE, MAX_CREDIT_MONTHS, \
    MAX_CREDIT_SUM
from estatebase.wrapper import get_wrapper, APARTMENT, NEWAPART, HOUSE, STEAD, \
    OUTBUILDINGS, AGRICULTURAL, FACILITIES, APARTMENTSTEAD, LANDSCAPING, GARAGE
from collections import OrderedDict
from django.template.base import Template
from django.utils.safestring import mark_safe
from django.template.context import Context
from django.utils.encoding import force_unicode
import re
from exportdata.utils import EstateTypeMapper, LayoutTypeMapper,\
    LayoutFeatureMapper
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,\
    GenericRelation    
from estatebase.lib import get_validity_delta, get_free_delta
from django.contrib.humanize.templatetags.humanize import naturaltime


class ExUser(User):     
    def __unicode__(self):
        return u'%s %s (%s)' % (self.first_name, self.last_name, self.username)
    class Meta:
        ordering = ['first_name','last_name']
        proxy = True

def get_profile_upload_to(instance, filename):    
    return os.path.join(u'userimages', force_unicode(instance.user), force_unicode(instance.id),  force_unicode(filename))


class UserProfile(models.Model):    
    user = models.OneToOneField(User)    
    geo_groups = models.ManyToManyField('GeoGroup', verbose_name=_('Geo group'),)
    office = models.ForeignKey('Office', blank=True, null=True, verbose_name=_('Office'), on_delete=models.PROTECT)
    phone = models.CharField(_('Phone'), max_length=255, blank=True, null=True,)
    image = ImageField(verbose_name=_('File'), upload_to=get_profile_upload_to, blank=True, null=True,)    
                    

class SimpleDict(models.Model):
    #objects = caching.base.CachingManager()
    name = models.CharField(_('Name'), unique=True, db_index=True, max_length=255)
    def __unicode__(self):
        return u'%s' % self.name
    def natural_key(self):
        return self.__unicode__()
    class Meta:
        ordering = ['name']
        abstract = True

class GeoGroup(SimpleDict):
    '''
    GeoGroup    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Geo group')
        verbose_name_plural = _('Geo groups')

class Region(SimpleDict):
    '''
    Район
    '''
    regular_name = models.CharField(_('Region'), max_length=100, blank=True, null=True)
    regular_name_gent = models.CharField(_('Gent'), max_length=100, blank=True, null=True)    
    geo_group = models.ForeignKey(GeoGroup, verbose_name=_('GeoGroup'), on_delete=models.PROTECT)
    metropolis = models.ForeignKey('Locality', verbose_name=_(u'Райцентр'), on_delete=models.PROTECT, related_name='metropolis_region', blank=True, null=True) 
    class Meta(SimpleDict.Meta):
        verbose_name = _('region')
        verbose_name_plural = _('regions')

class Office(SimpleDict):
    '''
    Офис
    '''
    regions = models.ManyToManyField(Region, verbose_name=_('Region'))
    address = models.TextField(_('Address'))
    address_short = models.TextField(_('Short address'))
    head = models.ForeignKey(ExUser, verbose_name=_('Head'), on_delete=models.PROTECT, blank=True, null=True) 
    class Meta(SimpleDict.Meta):
        verbose_name = _('Office')
        verbose_name_plural = _('Offices')

class Locality(models.Model):
    '''
    Населенный пункт
    '''
    CITY = 1
    name = models.CharField(_('Name'), db_index=True, max_length=255)
    name_gent = models.CharField(_('Gent'), max_length=255, blank=True, null=True)
    name_loct = models.CharField(_('Loct'), max_length=255, blank=True, null=True)
    region = models.ForeignKey(Region, blank=True, null=True, verbose_name=_('Region'), on_delete=models.PROTECT)
    locality_type = models.ForeignKey('LocalityType', blank=True, null=True, verbose_name=_('LocalityType'), on_delete=models.PROTECT)
    latitude = models.DecimalField(verbose_name=_('latitude'), max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(verbose_name=_('longitude'), max_digits=9, decimal_places=6, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.name
    def natural_key(self):
        return self.__unicode__()
    @property
    def office(self):
        return self.region.office_set.first()
    class Meta:
        verbose_name = _('locality')
        verbose_name_plural = _('localities')
        unique_together = ('name', 'region')
        ordering = ['name']  

class Microdistrict(models.Model):
    '''
    Микрорайоны в населенном пункте
    '''
    name = models.CharField(_('Name'), db_index=True, max_length=255)
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'), on_delete=models.PROTECT)
    is_address = models.BooleanField(u'Включать в адрес', default=False)
    def __unicode__(self):
        return u'%s' % self.name
    def natural_key(self):
        return self.__unicode__()
    class Meta:
        verbose_name = _('microdistrict')
        verbose_name_plural = _('microdistricts')
        unique_together = ('name', 'locality')
        ordering = ['name']

class Street(models.Model):
    '''
    Street
    '''
    name = models.CharField(_('Name'), db_index=True, max_length=255)
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'), on_delete=models.PROTECT)
    street_type = models.ForeignKey('StreetType', verbose_name=_('StreetType'), on_delete=models.PROTECT)
    def __unicode__(self):
        return u'%s %s' % (self.name, self.street_type or '')
    def natural_key(self):
        return self.__unicode__()
    class Meta:
        verbose_name = _('street')
        verbose_name_plural = _('streets')
        unique_together = ('name', 'locality', 'street_type')
        ordering = ['name']

class StreetType(SimpleDict):
    '''
    StreetType
    '''
    ULITSA = 1
    PEREULOK = 2
    PROSPEKT = 3
    PROEZD = 4
    SHOSSE = 5
    ALLEYA = 6
    TUPIK = 7
    BULVAR = 8
    sort_name = models.CharField(_('Short name'), db_index=True, max_length=50)
    def __unicode__(self):
        return u'%s' % self.sort_name
    class Meta(SimpleDict.Meta):        
        verbose_name = _('StreetType')
        verbose_name_plural = _('StreetTypes')

class Beside(SimpleDict):    
    '''
    Рассояние до (моря, речки и т.п.)
    '''
    name_gent = models.CharField(_('Gent'), max_length=255, blank=True, null=True)
    name_loct = models.CharField(_('Loct'), max_length=255, blank=True, null=True)
    name_dativ = models.CharField(_('Dativ'), max_length=255, blank=True, null=True)
    name_accus =models.CharField(_('Accus'), max_length=255, blank=True, null=True)
    class Meta(SimpleDict.Meta):
        verbose_name = _('beside')
        verbose_name_plural = _('besides')

class Electricity(SimpleDict):
    '''
    Электричество
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('electricity')
        verbose_name_plural = _('electricities')
        
class Watersupply(SimpleDict):
    '''
    Водоснабжение
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('watersupply')
        verbose_name_plural = _('watersupplies')

class Gassupply(SimpleDict):
    '''
    Газоснабжение
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('gassupply')
        verbose_name_plural = _('gassupplies')                

class Sewerage(SimpleDict):
    '''
    Канализация
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('sewerage')
        verbose_name_plural = _('sewerages')

class Telephony(SimpleDict):
    '''
    Телефония
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('telephony')
        verbose_name_plural = _('telephonies')
        
class Internet(SimpleDict):
    '''
    Интернет
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('internet')
        verbose_name_plural = _('internets')   

class Driveway(SimpleDict):
    '''
    Подъезд
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('driveway')
        verbose_name_plural = _('driveways')                      

class Document(SimpleDict):
    '''
    Документы
    '''
    estate_type_category = models.ManyToManyField('EstateTypeCategory', verbose_name=_('EstateTypeCategory'),)
    class Meta(SimpleDict.Meta):
        verbose_name = _('document')
        verbose_name_plural = _('documents')                      

class EstateParam(OrderedModel):
    '''
    Дополнительные параметры
    '''
    AVITO = 15
    RESTATE = 14
    POSTONSITE = 1
    IPOTEKA = 2
    PAYEXPORT = 16
    RENT = 11
    IDINAIDI = 19
    name = models.CharField(_('Name'), max_length=100)    
    def __unicode__(self):
        return u'%s' % self.name
    class Meta(OrderedModel.Meta):
        verbose_name = _('estate param')
        verbose_name_plural = _('estate params')            

class EstateStatus(SimpleDict):
    '''
    Статус объекта
    '''
    NEW = 2
    SOLD = 3
    REMOVED = 4
    DEPOSIT = 5    
    class Meta(SimpleDict.Meta):
        verbose_name = _('estate status')
        verbose_name_plural = _('estate statuses')         

class EstateClientStatus(SimpleDict):
    '''
    EstateClientStatus    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Estate client status')
        verbose_name_plural = _('Estate client statuss')

YES = 1
NO = 0
MAYBE = 2
AVAILABILITY_CHOICES = (
    (YES, u'Да'),
    (NO, u'Нет'),
    (MAYBE, u'Возможно'),
)

class EstateTypeCategory(OrderedModel):
    DOM = 2
    KVARTIRA = 4 
    U4ASTOK = 8
    KVARTIRAU4ASTOK = 5
    COMMERCE = 6    
    name = models.CharField(_('Name'), max_length=100)
    name_accs = models.CharField(_('Accs'), max_length=100, null=True)
    independent = models.BooleanField(_('Independent'), default=True)
    has_bidg = models.IntegerField(_('HasBidg'), choices=AVAILABILITY_CHOICES)
    has_stead = models.IntegerField(_('HasStead'), choices=AVAILABILITY_CHOICES)
    is_commerce = models.BooleanField(_('Commerce'), default=False)
    export_mark = models.BooleanField(u'Метка', default=False)        
    @property
    def maybe_stead(self):
        return self.has_stead == MAYBE
    @property
    def is_stead(self):
        return self.has_bidg == NO 
    @property
    def can_has_stead(self):
        return self.has_stead != NO
    def __unicode__(self):
        return u'%s' % self.name
    class Meta(OrderedModel.Meta):
        verbose_name = _('estate type category')
        verbose_name_plural = _('estate type categories')        

class EstateType(OrderedModel):     
    TEMPLATE_CHOICES = (
        (APARTMENT, u'Квартира'),
        (NEWAPART, u'Новостройка'),
        (HOUSE, u'Дом'),
        (STEAD, u'Участок'),
        (OUTBUILDINGS, u'Постройка'),
        (AGRICULTURAL, u'Сельхоз. участок'),
        (APARTMENTSTEAD, u'Квартира с участком'),
        (FACILITIES, u'Сооружение'),
        (LANDSCAPING, u'Благоустройство'),
        (GARAGE, u'Гараж')
        )   
    KOMNATA = 21 
    DACHA = 13
    name = models.CharField(_('Name'), max_length=100)
    name_accs = models.CharField(_('Accs'), max_length=100, null=True)
    estate_type_category = models.ForeignKey(EstateTypeCategory, verbose_name=_('EstateTypeCategory'), on_delete=models.PROTECT, related_name='types')   
    template = models.IntegerField(_('Template'), choices=TEMPLATE_CHOICES)
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255)
    placeable = models.BooleanField(_('Placeable'), default=True)        
    export_mark = models.BooleanField(u'Метка', default=True)        
    def __unicode__(self):
        return u'%s' % self.name    
    class Meta(OrderedModel.Meta):
        verbose_name = _('estate type')
        verbose_name_plural = _('estate types')
        ordering = ['estate_type_category__order', 'name']    
    
class HistoryMeta(models.Model):
    created = models.DateTimeField(_('Created'), db_index=True)
    created_by = models.ForeignKey(ExUser, verbose_name=_('User'), related_name='creators', on_delete=models.PROTECT)
    updated = models.DateTimeField(_('Updated'), blank=True, null=True, db_index=True)
    updated_by = models.ForeignKey(ExUser, verbose_name=_('Updated by'), blank=True, null=True, related_name='updators', on_delete=models.PROTECT)
    modificated = models.DateTimeField(_('Modificated'), db_index=True)
    
    @property
    def modificated_by(self):
        return self.updated_by if self.updated_by else self.created_by
    
    @property
    def user_id(self):
        return self.updated_by and self.updated_by.pk or self.created_by.pk                                        
    def save(self, *args, **kwargs):             
        self.modificated = self.updated or self.created                                                    
        super(HistoryMeta, self).save(*args, **kwargs)
    
def prepare_history(history, user_id):
    if not history:
        history = HistoryMeta()        
        history.created = datetime.datetime.now()
        history.created_by_id = user_id
        history.save() 
    elif user_id:
        history.updated = datetime.datetime.now()
        history.updated_by_id = user_id
        history.save()
    return history                 

class EstateClient(models.Model):
    ESTATE_CLIENT_STATUS = 3 #Собственник
    client = models.ForeignKey('Client')
    estate = models.ForeignKey('Estate')    
    estate_client_status = models.ForeignKey(EstateClientStatus, verbose_name=_('EstateClientStatus'))
    class Meta:
        unique_together = ('client', 'estate')       

class BaseModelManager(models.Manager):    
    def get_queryset(self):
        return super(BaseModelManager, self).get_queryset().filter(deleted=False)

class ProcessDeletedModel(models.Model):
    objects = BaseModelManager()
    all_objects = models.Manager()
    deleted = models.BooleanField(default=False)
    class Meta:
        abstract = True         

class ComStatus(SimpleDict):
    '''
    ComStatus    
    '''    
    status = models.IntegerField(_('Status'), choices=AVAILABILITY_CHOICES)
    class Meta(SimpleDict.Meta):
        verbose_name = _('Com status')
        verbose_name_plural = _('Com statuses')
    
class Validity(SimpleDict):
    '''
    Validity
    ./manage.py loaddata validity.json
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Validity')
        verbose_name_plural = _('Validitys')    
 
class EntranceEstate(models.Model):
    ENTRANCE = 1
    OVERLOOK = 2    
    DISTANCE = 3
    WINDOWVIEW = 4
    TYPE_CHOICES = (
        (ENTRANCE, u'Выход'),
        (OVERLOOK, u'Вид'),        
        (DISTANCE, u'Расстояние'),
        (WINDOWVIEW, u'Вид из окна'),
    )
    type = models.IntegerField(_('Type'), choices=TYPE_CHOICES) 
    distance = models.IntegerField(_('Distance'), blank=True, null=True)
    basic = models.BooleanField(_('Basic'), default=False)
    beside = models.ForeignKey('Beside', verbose_name=_('Object'))
    estate = models.ForeignKey('Estate',related_name='entranceestate_set')   
    class Meta:
        unique_together = ('beside', 'estate', 'type')
    
    def get_human_distance(self):
        if self.distance < 1000:
            return u'%g м' % self.distance
        else:
            return u'%g км' % round(self.distance/1000.0, 1)
    def get_human_desc(self):
        result = []        
        if self.type == self.ENTRANCE:
            e = self.beside.name_dativ if self.beside.name_dativ else self.beside.name
            result.append(u'выход к %s' % e)
        elif self.type == self.DISTANCE:
            o = self.beside.name_gent if self.beside.name_gent else self.beside.name
            result.append(u'расстояние до %s' % o)    
        elif self.type == self.WINDOWVIEW:
            o = self.beside.name_accus if self.beside.name_accus else self.beside.name
            result.append(u'вид из окон на %s' % o)
        elif self.type == self.OVERLOOK:
            o = self.beside.name_accus if self.beside.name_accus else self.beside.name
            result.append(u'вид на %s' % o)
        if self.distance:
            result.append(u'%s' % self.get_human_distance())            
        return ' '.join(result)
        
    
class Estate(ProcessDeletedModel):
    '''
    Базовая модель объектов недвижимости
    '''
    #Состояния адреса    
    NO_STREET = 1
    NO_NUMBER = 2
    NO_ADDRESS = 3
    ADDRESS_CHOICES = (
        (NO_STREET, u'Нет улицы'),
        (NO_NUMBER, u'Нет номера'),        
        (NO_ADDRESS, u'Нет адреса'),       
    )
    #Состояния
    FREE = 1
    NEW = 2
    SOLD = 3
    EXCLUDE = 4
    #Фазы
    VALID = 1
    NOTFREE = 2
    NOCONACT = 3
    DRAFT = 4
    EXPIRED = 5    
    #Базовые
    estate_category = models.ForeignKey(EstateTypeCategory, verbose_name=_('EstateCategory'), on_delete=models.PROTECT)
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.PROTECT) 
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'), on_delete=models.PROTECT, blank=True, null=True)
    microdistrict = models.ForeignKey('Microdistrict', verbose_name=_('Microdistrict'), blank=True, null=True, on_delete=models.SET_NULL)
    street = models.ForeignKey(Street, verbose_name=_('Street'), on_delete=models.PROTECT, blank=True, null=True)
    street_fake = models.ForeignKey(Street, verbose_name=u'Поддельная улица', on_delete=models.PROTECT, related_name='fake_streets', blank=True, null=True)
    address_state = models.PositiveIntegerField(verbose_name=_('Address state'), blank=True, null=True, choices=ADDRESS_CHOICES)    
    estate_number = models.CharField(_('Estate number'), max_length=10, blank=True, null=True)
    estate_number_fake = models.CharField(u'Поддельный номер', max_length=10, blank=True, null=True)
    clients = models.ManyToManyField('Client', verbose_name=_('Clients'), related_name='estates', through=EstateClient)
    origin = models.ForeignKey('Origin', verbose_name=_('Origin'), blank=True, null=True, on_delete=models.SET_NULL)
    beside = models.ForeignKey('Beside', verbose_name=_('Beside'), blank=True, null=True, on_delete=models.SET_NULL)
    beside_distance = models.PositiveIntegerField(_('Beside distance'), blank=True, null=True)
    entrances = models.ManyToManyField('Beside', verbose_name=_('Entrances'), blank=True, through=EntranceEstate, related_name='estates')
    saler_price = models.PositiveIntegerField(_('Saler price'), blank=True, null=True)
    agency_price = models.PositiveIntegerField(_('Agency price'), blank=True, null=True)
    estate_status = models.ForeignKey('EstateStatus', verbose_name=_('Estate status'), on_delete=models.PROTECT)
    com_status = models.ForeignKey(ComStatus, verbose_name=_('ComStatus'), blank=True, null=True)         
    #Коммуникации    
    electricity = models.ForeignKey('Electricity', verbose_name=_('Electricity'), blank=True, null=True, on_delete=models.SET_NULL)
    electricity_distance = models.PositiveIntegerField('Electricity distance', blank=True, null=True)
    watersupply = models.ForeignKey('Watersupply', verbose_name=_('Watersupply'), blank=True, null=True, on_delete=models.SET_NULL) 
    watersupply_distance = models.PositiveIntegerField(_('Watersupply distance'), blank=True, null=True)
    gassupply = models.ForeignKey('Gassupply', verbose_name=_('Gassupply'), blank=True, null=True, on_delete=models.SET_NULL)
    gassupply_distance = models.PositiveIntegerField(_('Gassupply distance'), blank=True, null=True)
    sewerage = models.ForeignKey('Sewerage', verbose_name=_('Sewerage'), blank=True, null=True, on_delete=models.SET_NULL)
    sewerage_distance = models.PositiveIntegerField(_('Sewerage distance'), blank=True, null=True)
    telephony = models.ForeignKey('Telephony', verbose_name=_('Telephony'), blank=True, null=True, on_delete=models.SET_NULL)
    internet = models.ForeignKey('Internet', verbose_name=_('Internet'), blank=True, null=True, on_delete=models.SET_NULL)
    driveway = models.ForeignKey('Driveway', verbose_name=_('Driveway'), blank=True, null=True, on_delete=models.SET_NULL)
    driveway_distance = models.PositiveIntegerField(_('Driveway distance'), blank=True, null=True)
    #Дополнительно    
    estate_params = models.ManyToManyField(EstateParam, verbose_name=_('Estate params'), blank=True, related_name='estates')    
    description = models.TextField(_('Description'), blank=True, null=True)
    client_description = models.TextField(_('Client description'), blank=True, null=True)
    comment = models.TextField (_('Comment'), blank=True, null=True, max_length=255)
    deal_status = models.ForeignKey('DealStatus', verbose_name=_('DealStatus'), blank=True, null=True, on_delete=models.SET_NULL)  
    #Изменения
    history = models.OneToOneField(HistoryMeta, blank=True, null=True, on_delete=models.SET_NULL)
    contact = models.ForeignKey('Contact', verbose_name=_('Contact'), blank=True, null=True, on_delete=models.SET_NULL)  
    validity = models.ForeignKey(Validity, verbose_name=_('Validity'), blank=True, null=True, on_delete=models.SET_NULL)
    broker = models.ForeignKey(ExUser, verbose_name=_('Broker'), blank=True, null=True, on_delete=models.SET_NULL)
    actualized = models.DateTimeField(_('Modificated'), db_index=True, default=datetime.date(2000, 1, 1))
    #attachments
    files = GenericRelation('EstateFile')
    links = GenericRelation('GenericLink')
    events = GenericRelation('GenericEvent', related_query_name='estates')
    #geo
    latitude = models.DecimalField(verbose_name=_('latitude'), max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(verbose_name=_('longitude'), max_digits=9, decimal_places=6, blank=True, null=True)
    
    def delete(self):
        self.deleted = True
        self.save()
    
    def get_absolute_url(self):
        return self.detail_link     
            
    def check_contact(self):
        return self.contact and self.contact.contact_state_id in (Contact.AVAILABLE, Contact.NOTRESPONDED, Contact.NONAVAILABLE)
     
    def check_validity(self):        
        post_on_site = len(self.estate_params.filter(pk=EstateParam.POSTONSITE)) > 0        
        AGRICULTURAL_STEAD = self.basic_stead and self.basic_stead.estate_type.template == AGRICULTURAL
        report = OrderedDict([(self.NOTFREE, False), (self.NOCONACT, False), (self.DRAFT, [])])
        report[self.NOCONACT] = not self.check_contact() 
        if not self.estate_status_id == self.FREE:
            report[self.NOTFREE] = True    
        if not self.street and not self.address_state in (self.NO_STREET, self.NO_ADDRESS) and not AGRICULTURAL_STEAD:
            report[self.DRAFT].append(unicode(_('Street')))
        if not self.estate_number and not self.address_state in (self.NO_NUMBER, self.NO_ADDRESS) and not AGRICULTURAL_STEAD:
            report[self.DRAFT].append(unicode(_('Estate number')))    
        if post_on_site and not self.client_description:
            report[self.DRAFT].append(u'Описание заказчику')
#             if not (self.basic_stead and (self.basic_stead.estate_type.template == AGRICULTURAL or self.basic_stead.estate_type_id == EstateTypeMapper.DACHNYYUCHASTOK)): 
#                 if not (self.basic_bidg and self.basic_bidg.estate_type_id in (EstateTypeMapper.DACHA, EstateTypeMapper.GARAZH, EstateTypeMapper.LODOCHNYYGARAZH)):
        if not self.microdistrict:
            report[self.DRAFT].append(unicode(_('Microdistrict')))            
        if not self.watersupply:
            report[self.DRAFT].append(unicode(_('Watersupply')))
        if not self.gassupply:
            report[self.DRAFT].append(unicode(_('Gassupply')))    
        if not self.electricity:
            report[self.DRAFT].append(unicode(_('Electricity')))    
        if not self.agency_price:
            report[self.DRAFT].append(unicode(_('Agency price')))
        if self.basic_bidg and self.basic_bidg.is_independent:
            if not self.basic_bidg.year_built:
                report[self.DRAFT].append(unicode(_('Year built')))
            if not self.basic_bidg.floor and not self.basic_bidg.estate_type.template in (HOUSE, OUTBUILDINGS, GARAGE):                                
                report[self.DRAFT].append(unicode(_('Floor')))
            if not self.basic_bidg.floor_count:
                report[self.DRAFT].append(unicode(_('Floor count')))
            if not self.basic_bidg.wall_construcion:
                report[self.DRAFT].append(unicode(_('Wall construcion')))
            if not self.basic_bidg.room_count:
                report[self.DRAFT].append(unicode(_('Room count')))
            if not self.basic_bidg.total_area:
                report[self.DRAFT].append(unicode(_('Total area')))
            if not self.basic_bidg.interior:
                report[self.DRAFT].append(unicode(_('Interior')))
            
            if self.estate_category_id == EstateTypeCategory.KVARTIRA: 
                if self.basic_bidg.estate_type_id not in (EstateTypeMapper.KOMNATA, EstateTypeMapper.KVARTIRASTUDIYA): 
                    if not self.basic_bidg.get_kuhnya_area():
                        report[self.DRAFT].append(u'Площадь кухни в планировке')
            
            if self.estate_category_id in (EstateTypeCategory.DOM, EstateTypeCategory.KVARTIRA, EstateTypeCategory.KVARTIRAU4ASTOK):                
                if self.basic_bidg.estate_type_id not in (EstateTypeMapper.DACHA,):                 
                    if not self.basic_bidg.used_area:
                        report[self.DRAFT].append(unicode(_('Used area')))
                    
        if self.basic_stead:
            if not self.basic_stead.total_area:
                report[self.DRAFT].append(u'Площадь участка')        
            if not self.basic_stead.face_area:
                report[self.DRAFT].append(u'Фасад')        
        return report
    
    def get_actual_date(self):
        if self.contact:
            return self.contact.updated        
        return self.history.modificated
        
    def actualize(self):
        self.actualized = self.get_actual_date()        
        
    def set_validity(self, report):
        self.validity_id = self.VALID
        self.actualize()
        for key, value in report.items():
            if value:
                self.validity_id = key
                break
        
    @property
    def validity_report(self):
        result = []
        report = self.check_validity()
        if report[self.NOTFREE]:
            result.append(u'Не вакантно')
        if report[self.NOCONACT]:    
            result.append(u'Нет доступного контакта')
        if report[self.DRAFT]:
            result.append(u'не заполнены поля: %s' % ', '.join(report[self.DRAFT]))
        return '; '.join(result).lower()
    @property
    def validity_state(self):        
        if not self.correct and self.validity_id == self.VALID:
            return u'Устарело'
        else:
            return self.validity
        return u'Корректно'
            
    @property
    def detail_link(self):            
        return reverse('estate_list_details', args=[self.pk]) 
    
    @property
    def basic_bidg(self):        
        bidgs = list(self.bidgs.filter(basic__exact=True)[:1])        
        if bidgs:
            return bidgs[0]
        elif not self.estate_category.is_stead:
            bidgs = list(self.bidgs.filter(estate_type__estate_type_category__independent=True)[:1])
            if bidgs:
                if bidgs[0].is_independent:                    
                    return bidgs[0]
                                                  
    @property
    def basic_stead(self):        
        try:
            return self.stead
        except Stead.DoesNotExist:
            return None    
    @property
    def correct(self):         
        return self.validity_id == self.VALID and (self.actualized > get_validity_delta())
    
    @property
    def expired(self):        
        return self.validity_id == self.VALID and (self.actualized <= get_validity_delta())
    
    @property
    def is_free(self):       
        return self.validity_id == self.VALID and (self.actualized < get_free_delta())
    
    @property
    def basic_contact(self):
        return self.contact 
    
    @property
    def state_css(self):
        css = {self.FREE:'free-state', self.NEW:'new-state', self.SOLD:'sold-state', self.EXCLUDE:'exclude-state'}                             
        return self.estate_status_id in css and css[self.estate_status_id] or ''    
    def get_best_contact(self):
        contacts = Contact.objects.filter(client__estates__id__exact=self.pk, client__deleted=False).select_related().order_by('contact_state__id', 'contact_type__id', '-updated')[:1]        
        if contacts:
            return contacts[0]
    
    @property
    def estate_type(self):
        return self.estate_type_base()
    
    @property
    def estate_type_accs(self):
        return self.estate_type_base(field='name_accs')

    @property
    def basic_estate_type(self):        
        if self.estate_category.is_stead and self.basic_stead:
            return self.basic_stead.estate_type
        else:
            if self.basic_bidg:
                return self.basic_bidg.estate_type

    @property
    def basic_estate_type_mark(self):        
        if self.estate_category.is_stead and self.basic_stead:
            return self.basic_stead.estate_type.export_mark
        else:
            if self.basic_bidg:
                return self.basic_bidg.estate_type.export_mark                

    @property
    def basic_estate_type_accs(self):        
        if self.estate_category.is_stead and self.basic_stead:
            return self.basic_stead.estate_type.name_accs
        else:
            if self.basic_bidg:
                return self.basic_bidg.estate_type.name_accs
                
    @property
    def estate_type_total_area(self):
        complex_name_format = u'%s %g %s'
        attr = {
                'stead' : {'name':'total_area_sotka', 'mesure': u'сот.', 'format' : complex_name_format},
                'bidg' : {'name':'total_area', 'mesure': u'м.кв.', 'format' : complex_name_format},
                }
        return self.estate_type_base(attr)
    def apply_attr(self, obj, attr, field):
        complex_name = getattr(obj.estate_type, field)                
        if attr:
            attr_value = getattr(obj, attr['name']) or None
            if attr_value: 
                complex_name = attr['format'] % (complex_name, attr_value, attr['mesure'])                
        return complex_name
    def estate_type_base(self, attr=None, field='name'):        
        if self.estate_category.is_stead:
            return self.apply_attr(self.stead, attr['stead'] if attr else None, field) 
        else:
            result = []
            for bidg in self.bidg_objects:                                 
                result.append(self.apply_attr(bidg, attr['bidg'] if attr else None, field))
            if len(result):          
                return ', '.join(result)
            else:
                return self.estate_category     
            
    @property
    def bidg_objects(self):
        return self.bidgs.filter(estate_type__estate_type_category__independent=True) 
    @property
    def bidg_outbuildings(self):
        return self.bidgs.filter(estate_type__estate_type_category__independent=False)                               
    @property
    def is_commerce(self):
        return self.com_status.status == YES
    @property
    def max_credit_sum(self):
        return int(self.agency_price - self.agency_price * MAX_CREDIT_SUM)
    @property
    def credit_sum(self):        
        return int(self.max_credit_sum * INTEREST_RATE / 12 / (1 - pow((1 + INTEREST_RATE / 12), -MAX_CREDIT_MONTHS)))
    def __unicode__(self):
        return u'%s' % self.pk    
    
    def set_contact(self):
        self.contact = self.get_best_contact()
        self.set_validity(self.check_validity())
            
    @property
    def get_not_basic_bidgs(self):
        return self.bidgs.exclude(basic__exact=True)   
    
    @property
    def is_web_published(self):
        try:
            wp_meta = self.wp_meta             
            return len(wp_meta.post_id) > 0
        except:
            return False
    
    @property
    def modificated(self):
        return self.actualized 
    
    @property 
    def agency_price_1000(self):
        if self.agency_price:
            return int(self.agency_price / 1000)
     
    def event_dict(self, event):
        result = event.event_dict() 
        color = '#81c784'
        brocker_color = '#4caf50'
        historical_color = '#cccccc'        
        if event.is_last({ 'estates': self }):            
            result['color'] = brocker_color if event.content_object.broker else color
        else:
            result['color'] = historical_color
        return result 
    
    def can_change(self, user):
        if not self.is_free and not user.has_perm('estatebase.change_broker'):
            if self.broker and self.broker.is_active and not user == self.broker:
                return False
        return True
                        
    class Meta:
        unique_together = [
            ('id', 'agency_price', 'actualized', 'estate_category'),
        ]
        verbose_name = _('estate')
        verbose_name_plural = _('estate')
        ordering = ['-id']    
        permissions = (
            ("view_private", u'Просмотр цены, полного адреса и контактов'),
            ("change_broker", u'Может назначать риэлтора'),
        )

def get_upload_to(instance, filename):    
    return os.path.join(u'photos',  force_unicode(instance.estate_id),  force_unicode(filename))

class EstatePhoto(OrderedModel):
    '''
    Фото
    '''
    estate = models.ForeignKey(Estate, verbose_name=_('Estate'), related_name='images')
    name = models.CharField(_('Name'), max_length=100, blank=True, null=True,)
    note = models.CharField(_('Note'), max_length=255, blank=True, null=True,)
    image = ImageField(upload_to=get_upload_to)
    def __unicode__(self):
        return u'%s' % (self.name or self.image.name)
    class Meta(OrderedModel.Meta):
        verbose_name = _('EstatePhoto')
        verbose_name_plural = _('EstatePhotos') 

def get_file_upload_to(instance, filename):    
    return os.path.join(u'files', force_unicode(instance.content_type.id), force_unicode(instance.object_id),  force_unicode(filename))


class DocumentType(SimpleDict):
    '''
    Типы присоединенных файлов     
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Document type')
        verbose_name_plural = _('Document types')
    

class EstateFile(OrderedModel):
    '''
    Файлы
    '''
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(_('Name'), max_length=100, blank=True, null=True,)
    note = models.CharField(_('Note'), max_length=255, blank=True, null=True,)
    file = models.FileField(verbose_name=_('File'), upload_to=get_file_upload_to)
    document_type = models.ForeignKey(DocumentType, verbose_name=_('Document type'), blank=True, null=True, on_delete=models.SET_NULL)
    def __unicode__(self):
        return u'%s' % (self.name or self.file.name)
    class Meta(OrderedModel.Meta):
        verbose_name = _('EstateFile')
        verbose_name_plural = _('EstateFiles')
    def is_image(self):
        import imghdr        
        return imghdr.what(self.file.path) is not None 


class GenericLink(models.Model):
    '''
    Ссылки
    '''
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(_('Name'), max_length=100, blank=True, null=True,)
    url = models.CharField(_('Url'), max_length=100, blank=True, null=True,)
    note = models.CharField(_('Note'), max_length=255, blank=True, null=True,)    
    def __unicode__(self):
        return u'%s' % (self.name or self.url)
    class Meta:
        verbose_name = _('GenericLink')
        verbose_name_plural = _('GenericLinks')


class Supply(SimpleDict):
    '''
    Перечень коммуникаций    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Supply')
        verbose_name_plural = _('Supply')


class SupplyState(SimpleDict):
    '''
    Сотояние коммуникаций    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Supply state')
        verbose_name_plural = _('Supply states')

class GenericSupply(models.Model):
    '''
    Коммуникации
    '''
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    supply = models.ForeignKey(Supply, verbose_name=_('Supply'))
    supply_state = models.ForeignKey(SupplyState, verbose_name=_('Supply state'), blank=True, null=True,)
    distance = models.PositiveIntegerField(verbose_name=_('Distance'), blank=True, null=True,)
        
    def __unicode__(self):
        return u'%s' % (self.supply)
    class Meta:
        verbose_name = _('Supply')
        verbose_name_plural = _('Supply')        
    
class WallConstrucion(SimpleDict):
    '''
    Стены
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('wall construcion')
        verbose_name_plural = _('wall construcions') 

class ExteriorFinish(SimpleDict):
    '''
    Внешняя оттелка
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('exterior finish')
        verbose_name_plural = _('exterior finishs') 

class WindowType(SimpleDict):
    '''
    Окна
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('window type')
        verbose_name_plural = _('window types')

class Roof(SimpleDict):
    '''
    Крыша    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Roof')
        verbose_name_plural = _('Roofs')

class Heating(SimpleDict):
    '''
    Отопление
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('heating')
        verbose_name_plural = _('heatings')  

class WallFinish(SimpleDict):
    '''
    Внутренняя оттелка стен    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Wall finish')
        verbose_name_plural = _('Wall finishs')

class Flooring(SimpleDict):
    '''
    Пол    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Flooring')
        verbose_name_plural = _('Floorings')

class Ceiling(SimpleDict):
    '''
    Потолок
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Ceiling')
        verbose_name_plural = _('Ceilings')

class Interior(SimpleDict):
    '''
    Внутренняя оттелка (ремонт)   
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Interior')
        verbose_name_plural = _('Interiors')

def validate_year(value):
    if not 2100 > value > 1800:
        raise ValidationError(u'Значение года указано не верно.')

class LevelName(SimpleDict):
    '''
    Назание этажа    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Level name')
        verbose_name_plural = _('Level names')

class Level(models.Model):
    '''
    Планоровка этажей
    '''     
    level_name = models.ForeignKey(LevelName, verbose_name=_('Level name'))
    bidg = models.ForeignKey('Bidg', verbose_name=_('Level'), related_name='levels')    
    class Meta:
        verbose_name = _('Level')
        verbose_name_plural = _('Levels')
        ordering = ['level_name']
    def __unicode__(self):
        return u'%s' % self.level_name    

class LayoutType(SimpleDict):
    '''
    Вид объекта планировки    
    '''
    LIVING_SPACE = 1
    KITCHEN_SPACE = 2    
    CATEGORY_CHOICES = (
        (LIVING_SPACE, u'Жилая площадь'),
        (KITCHEN_SPACE, u'Кухня'),        
    )    
    layout_category = models.IntegerField(_('Category'), choices=CATEGORY_CHOICES, blank=True, null=True,)
    class Meta(SimpleDict.Meta):
        verbose_name = _('Layout type')
        verbose_name_plural = _('Layout types')

class Furniture(SimpleDict):
    '''
    Мебель    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Furniture')
        verbose_name_plural = _('Furnitures')

class LayoutFeature(SimpleDict):
    '''
    LayoutFeature    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Layout feature')
        verbose_name_plural = _('Layout features')

class Layout(models.Model):
    level = models.ForeignKey(Level, verbose_name=_('Level'))
    layout_type = models.ForeignKey(LayoutType, verbose_name=_('LayoutType'), on_delete=models.PROTECT)
    area = models.DecimalField(_('Area'), blank=True, null=True, max_digits=7, decimal_places=2)
    furniture = models.ForeignKey(Furniture, verbose_name=_('Furniture'), blank=True, null=True, on_delete=models.PROTECT)
    layout_feature = models.ForeignKey(LayoutFeature, verbose_name=_('LayoutFeature'), blank=True, null=True, on_delete=models.PROTECT)
    interior = models.ForeignKey(Interior, verbose_name=_('Interior'), blank=True, null=True, on_delete=models.PROTECT)
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255)   
    class Meta:
        verbose_name = _('layout')
        verbose_name_plural = _('layouts')        
        ordering = ['id']     

class Appliance(SimpleDict):
    '''
    Appliance
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Appliance')
        verbose_name_plural = _('Appliances')
    

class Bidg(models.Model):
    _layout = None 
    _layout_living_area = None    
    estate = models.ForeignKey(Estate, verbose_name=_('Estate'), related_name='bidgs')
    estate_type = models.ForeignKey(EstateType, verbose_name=_('EstateType'), on_delete=models.PROTECT)   
    room_number = models.CharField(_('Room number'), max_length=10, blank=True, null=True)
    year_built = models.PositiveIntegerField(_('Year built'), blank=True, null=True, validators=[validate_year])
    floor = models.PositiveIntegerField(_('Floor'), blank=True, null=True)
    floor_count = models.DecimalField(_('Floor count'), blank=True, null=True, max_digits=3, decimal_places=1)
    elevator = models.BooleanField(_('Elevator'), default=False)
    wall_construcion = models.ForeignKey(WallConstrucion, verbose_name=_('Wall construcion'), blank=True, null=True, on_delete=models.PROTECT)
    exterior_finish = models.ForeignKey(ExteriorFinish, verbose_name=_('Exterior finish'), blank=True, null=True, on_delete=models.PROTECT)    
    window_type = models.ForeignKey(WindowType, verbose_name=_('Window type'), blank=True, null=True, on_delete=models.PROTECT)
    roof = models.ForeignKey(Roof, verbose_name=_('Roof'), blank=True, null=True, on_delete=models.PROTECT)
    heating = models.ForeignKey(Heating, verbose_name=_('Heating'), blank=True, null=True, on_delete=models.PROTECT)
    ceiling_height = models.DecimalField(_('Ceiling height'), blank=True, null=True, max_digits=5, decimal_places=2)
    room_count = models.PositiveIntegerField(_('Room count'), blank=True, null=True)
    total_area = models.DecimalField(_('Total area'), blank=True, null=True, max_digits=10, decimal_places=2)
    used_area = models.DecimalField(_('Used area'), blank=True, null=True, max_digits=10, decimal_places=2)
    documents = models.ManyToManyField(Document, verbose_name=_('Documents'), blank=True)
    #Внутренняя отделка    
    wall_finish = models.ForeignKey(WallFinish, verbose_name=_('WallFinish'), blank=True, null=True, on_delete=models.PROTECT)
    flooring = models.ForeignKey(Flooring, verbose_name=_('Flooring'), blank=True, null=True, on_delete=models.PROTECT)
    ceiling = models.ForeignKey(Ceiling, verbose_name=_('Ceiling'), blank=True, null=True, on_delete=models.PROTECT)
    interior = models.ForeignKey(Interior, verbose_name=_('Interior'), blank=True, null=True, on_delete=models.PROTECT)
    appliances = models.ManyToManyField(Appliance,verbose_name=_('Appliance'),blank=True)
    #Новостройка
    yandex_building = models.ForeignKey('YandexBuilding', verbose_name=_('YandexBuilding'), blank=True, null=True, on_delete=models.PROTECT)
    #param
    basic = models.BooleanField(_('Basic'), default=False, editable=True)    
    description = models.TextField(_('Description'), blank=True, null=True)    
    class Meta:
        verbose_name = _('bidg')
        verbose_name_plural = _('bidgs')
        ordering = ['id']
    @property    
    def layout_area(self):
        return Layout.objects.filter(level__in=self.levels.all()).aggregate(Sum('area'))['area__sum']    
    @property    
    def layout_living_area(self):
        if not self._layout_living_area:
            l = self.get_layout()        
            self._layout_living_area = sum(l.get('rooms_area'))
        return self._layout_living_area
    @property    
    def is_facility(self):
        return self.estate_type.template in [FACILITIES, LANDSCAPING]
    @property
    def is_independent(self):
        return self.estate_type.estate_type_category.independent
    def __unicode__(self):
        return u'%s' % self.pk
    
    def get_layout(self):
        if self._layout is None:           
            layouts = list(Layout.objects.filter(level__bidg=self))            
            result = {}
            kuhnya_area = 0
            sanuzel_sovmest = 0
            sanuzel_razdel = 0
            room_izol = 0
            room_smezh = 0
            balcons = 0
            loggias = 0
            rooms_space = []
            room_furniture = False
            kitchen_furniture = False
            for l in layouts:                 
                if l.layout_type.layout_category in (LayoutType.KITCHEN_SPACE,):
                    if l.area:
                        kuhnya_area += l.area
                    if l.furniture:
                        kitchen_furniture = True
                if l.layout_type.layout_category in (LayoutType.LIVING_SPACE,):
                    if l.area:
                        rooms_space.append(l.area)
                    if l.layout_feature_id == LayoutFeatureMapper.IZOLIROVANNAYA:
                        room_izol += 1
                    elif l.layout_feature_id == LayoutFeatureMapper.SMEZHNAYA:
                        room_smezh += 1
                    if l.furniture:
                        room_furniture = True                                             
                if l.layout_type_id in (LayoutTypeMapper.SANUZEL,):
                    if l.layout_feature_id == LayoutFeatureMapper.SOVMESCHENNYY:
                        sanuzel_sovmest += 1
                    else:
                        sanuzel_razdel += 1           
                if l.layout_type_id in (LayoutTypeMapper.BALKON,):
                    balcons += 1
                if l.layout_type_id in (LayoutTypeMapper.LODZHIYA,):
                    loggias += 1                                        
            result['kuhnya_area'] = kuhnya_area
            result['rooms_area'] = rooms_space
            result['sanuzel_sovmest'] = sanuzel_sovmest
            result['sanuzel_razdel'] = sanuzel_razdel
            result['balcons'] = balcons
            result['loggias'] = loggias
            result['room_izol'] = room_izol
            result['room_smezh'] = room_smezh                         
            result['room_furniture'] = room_furniture
            result['kitchen_furniture'] = kitchen_furniture
            self._layout = result
        return self._layout
    
    def get_layout_key(self, key):
        layout = self.get_layout()
        if layout:
            return layout[key]

    def get_room_izol(self):
        return self.get_layout_key('room_izol')
    
    def get_room_smezh(self):
        return self.get_layout_key('room_smezh')
    
    def get_kuhnya_area(self):
        return self.get_layout_key('kuhnya_area')
    
    def get_kitchen_furniture(self):
        return self.get_layout_key('kitchen_furniture')
    
    def get_room_furniture(self):
        return self.get_layout_key('room_furniture')
        
    def get_rooms_area(self):
        return self.get_layout_key('rooms_area')
        
    def get_sanuzel_sovmest_count(self):
        return self.get_layout_key('sanuzel_sovmest')
    
    def get_sanuzel_razdel_count(self):
        return self.get_layout_key('sanuzel_razdel')
    
    def get_balcons_count(self):
        return self.get_layout_key('balcons')
    
    def get_loggias_count(self):
        return self.get_layout_key('loggias')
    
class Shape(SimpleDict):
    '''
    Shape    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Shape')
        verbose_name_plural = _('Shapes')

class LandType(SimpleDict):
    '''
    LandType    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Land type')
        verbose_name_plural = _('Land types')

class Purpose(SimpleDict):
    '''
    Purpose    
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Purpose')
        verbose_name_plural = _('Purposes')

class Stead(models.Model):     
    DEFAULT_TYPE_ID = 15   
    estate = models.OneToOneField(Estate, verbose_name=_('Estate'), related_name='stead')
    estate_type = models.ForeignKey(EstateType, verbose_name=_('EstateType'), limit_choices_to={'estate_type_category__has_bidg': False}, default=DEFAULT_TYPE_ID, on_delete=models.PROTECT)  
    total_area = models.DecimalField(_('Total area'), blank=True, null=True, max_digits=10, decimal_places=2)      
    face_area = models.DecimalField(_('Face area'), blank=True, null=True, max_digits=10, decimal_places=2)
    shape = models.ForeignKey(Shape, verbose_name=_('Shape'), blank=True, null=True, on_delete=models.PROTECT)
    land_type = models.ForeignKey(LandType, verbose_name=_('LandType'), blank=True, null=True, on_delete=models.PROTECT)
    purpose = models.ForeignKey(Purpose, verbose_name=_('Purpose'), blank=True, null=True, on_delete=models.PROTECT)
    documents = models.ManyToManyField(Document, verbose_name=_('Documents'), blank=True)
    cadastral_number = models.CharField(_('Cadastral number'), max_length=150, blank=True, null=True)    
    class Meta:
        verbose_name = _('stead')
        verbose_name_plural = _('steads')
    @property
    def field_list(self):
        wrapper = get_wrapper(self)                          
        return wrapper.field_list()
    @property
    def total_area_sotka(self):
        if self.total_area:
            return float(self.total_area / 100)

class ClientType(SimpleDict):    
    class Meta(SimpleDict.Meta):
        verbose_name = _('client type')
        verbose_name_plural = _('client types')

class Origin(SimpleDict):
    '''
    Источник      
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('origin')
        verbose_name_plural = _('origins')

class Client(ProcessDeletedModel):
    """
    An client entity      
    """
    name = models.CharField(_('Name'), max_length=255)
    client_type = models.ForeignKey(ClientType, verbose_name=_('ClientType'), on_delete=models.PROTECT)
    origin = models.ForeignKey(Origin, verbose_name=_('Origin'), blank=True, null=True, on_delete=models.PROTECT) 
    address = models.CharField(_('Address'), blank=True, null=True, max_length=255)
    note = models.TextField(_('Note'), blank=True, null=True) 
    history = models.OneToOneField(HistoryMeta, blank=True, null=True, editable=False)    
    has_dev_profile = models.BooleanField(_('HasDevProfile'), default=False)
    dev_profile = models.OneToOneField('devrep.DevProfile', verbose_name=_('DevProfile'), blank=True, null=True, related_name='client', on_delete=models.SET_NULL)
    extra_profile = models.OneToOneField('devrep.ExtraProfile', verbose_name=_('ExtraProfile'), blank=True, null=True, related_name='client', on_delete=models.SET_NULL)
    events = GenericRelation('GenericEvent', related_query_name='clients')    
    
    def __unicode__(self):
        return u'%s: %s' % (self.name, ', '.join(self.contacts.all().values_list('contact', flat=True)))    
    
    @property
    def user(self):
        return self.history.updated_by or self.history.created_by
    
    def get_absolute_url(self):            
        return reverse('client_detail', args=[self.pk])

    def event_dict(self, event): 
        color = '#db960d'        
        historical_color = '#cccccc'
        result = event.event_dict()        
        if event.is_last({ 'clients': self }):            
            result['color'] = color
        else:
            result['color'] = historical_color
        return result
    
    def can_change(self, user):        
        return True   
                    
    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')
        ordering = ['-id']

class ContactType(SimpleDict):
    class Meta(SimpleDict.Meta):
        verbose_name = _('contact type')
        verbose_name_plural = _('contact types')

class ContactState(SimpleDict):
    class Meta(SimpleDict.Meta):
        verbose_name = _('contact state')
        verbose_name_plural = _('contact states')

class ContactHistory(models.Model):
    event_date = models.DateTimeField(_('Event Date'), auto_now_add=True)
    user = models.ForeignKey(ExUser, verbose_name=_('User'), blank=True, null=True, on_delete=models.PROTECT)
    contact_state = models.ForeignKey(ContactState, verbose_name=_('Contact State'), on_delete=models.PROTECT) 
    contact = models.ForeignKey('Contact', verbose_name=_('Contact'), on_delete=models.CASCADE)
    def __unicode__(self):
        return u'%s: %s' % (self.event_date, self.contact_state.name)
    class Meta:
        verbose_name = _('contact history')
        verbose_name_plural = _('contact history') 

class Contact(models.Model):
    AVAILABLE = 1
    NONAVAILABLE = 2
    BAN = 3
    NOTRESPONDED = 4
    NOTCHECKED = 5   
    PHONE = 1
    EMAIL = 2
    SITE = 3
    client = models.ForeignKey(Client, verbose_name=_('Client'), related_name='contacts')
    contact_type = models.ForeignKey(ContactType, verbose_name=_('ContactType'), on_delete=models.PROTECT)
    contact = models.CharField(_('Contact'), max_length=255, db_index=True, unique=True)
    updated = models.DateTimeField(_('Updated'), blank=True, null=True, db_index=True)   
    contact_state = models.ForeignKey(ContactState, verbose_name=_('Contact State'), default=NOTCHECKED, on_delete=models.PROTECT)
    user_id = None
    migration = False     
    def __unicode__(self):
        return u'%s (%s)' % (self.contact, self.client.name)
    @property
    def state_css(self):
        css = {self.AVAILABLE:'available-state', self.NONAVAILABLE:'non-available-state', self.BAN:'ban-state', self.NOTRESPONDED:'not-responded-state', self.NOTCHECKED:'not-checked-state'}                             
        return self.contact_state.pk in css and css[self.contact_state.pk] or ''                
    def clean(self):        
        self.contact = self.contact.strip()
        contact_type = None
        try: 
            contact_type = self.contact_type
        except ContactType.DoesNotExist:
            pass        
               
        if contact_type and contact_type.id == self.PHONE:
            self.contact = re.sub(r'\D', '', self.contact)            
            
        q = Contact.objects.filter(contact__iexact=self.contact)
        if self.id:
            q = q.exclude(pk=self.id)
        if q.count() > 0:
            client = list(q.all()[:1])[0].client
            extra = ''
            t = None
            if not client.deleted:
                t = Template(u'<a title="Показать карточку клиента в оттельном окне..." target="_blank" href="{% url "client_detail" pk %}">[{{ pk }}] {{ name }}</a>')
                t = t.render(Context({ 'name': client.name, 'pk': client.pk }))
            else:
                t = '"[%s] %s"' % (client.pk, client.name)                
                extra = u' - находится в корзине! %s'
                restore = Template(u'<a target="_blank" href="{% url "client_restore" pk %}">Восстановить</a>')
                extra = extra % restore.render(Context({ 'pk': client.pk }))
            raise ValidationError(mark_safe(u'Данный контакт уже создан и принадлежит %s %s' % (t, extra)))
                     
        if not contact_type:
            raise ValidationError(u'Вид контакта не может оставаться пустым!')
        validate_url = URLValidator()
        validate_phone = RegexValidator(regex=r'^8\d{8,}$')        
        if self.contact_type.id == self.PHONE:            
            validate_phone(self.contact)
        elif self.contact_type.id == self.EMAIL:
            validate_email(self.contact)
        elif self.contact_type.id == self.SITE:
            validate_url(self.contact)
    def save(self, *args, **kwargs):
        if not self.migration:               
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
                                         user_id=self.user_id,
                                         )
        contact_history.save()                                                            
    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts') 
        ordering = ['contact_state__id', 'contact_type__id']


class BidState(models.Model):
    '''
    новая - добавлена офис-менеджером и не определена риэлтору, дополнительный статус - устаревшая, назначается по истечении 30 дней
    свободная - риэлтор отдал заявку или руководитель очистил список риэлторов по заявке, либо, если пользователь делается неактивным, все его заявки становятся свободными, дополнительный статус - устаревшая, назначается по истечении 30 дней
    в работе -  заявка закреплена за одним или несколькими риэлторами, данное состояние имеет дополнительный статус - просрочена, который назначается по дате события
    в ожидании - заявки, которые обновлялись последний раз ранее 01.12.2015 года
    закрыта - категория статуса заявки неактуальные
        
    свободный список (аукцион) = новая + свободная + просрочена
    '''   
    
    FREEDAYS = 3 
    PENDING_DATE = datetime.datetime(2015,12,1)
           
    NEW = 1
    FREE = 2
    OUTDATED = 21
    WORKING = 3
    EXPIRED = 31
    PENDING = 4
    CLOSED = 5 
    
    
    STATE_CHOICES = (
        (NEW, u'новая'),
        (FREE, u'свободная'),        
        (WORKING, u'в работе'),
        (PENDING, u'в ожидании'),
        (CLOSED, u'закрыта'),
    )
    
    bid = models.OneToOneField('Bid',verbose_name=_('Bid'), related_name='state')
    state = models.PositiveIntegerField(verbose_name=_('State'), default=NEW, choices=STATE_CHOICES, db_index=True)
    event_date = models.DateTimeField(verbose_name=_('Event date'), blank=True, null=True, db_index=True)
    
    class Meta:
        index_together = [
            ["state", "event_date"],
        ]
        
    @staticmethod
    def get_free_date():
        return datetime.datetime.now()
        
    @property    
    def is_expired(self):
        return self.event_date < BidState.get_free_date() and self.state == BidState.WORKING 
    
    @staticmethod
    def calculate_state(bid, event_date):        
        if bid.is_closed():
            return BidState.CLOSED
        
        if bid.history and bid.history.modificated < BidState.PENDING_DATE:        
            return BidState.PENDING
        
        last_event = bid.get_last_event()
        if last_event and last_event.is_free():
            return BidState.FREE
        
        if not last_event and not bid.brokers.exists():
            return BidState.NEW  
        
        if not bid.brokers.exists():
            return BidState.FREE
                 
        return BidState.WORKING        
    
    @staticmethod
    def update_state(bid):
        if not bid:
            return
        try:
            state = bid.state
        except BidState.DoesNotExist:
            state = None 
        if not state:
            state = BidState()
            state.bid = bid 
        
        last_calendar_event = bid.get_last_calendar_event()
        if last_calendar_event and last_calendar_event.date:
            event_date = last_calendar_event.date
        elif bid.history and bid.history.modificated:            
            event_date = bid.history.modificated
        else:
            event_date = datetime.datetime.now()
        
        event_date = event_date + datetime.timedelta(days=BidState.FREEDAYS)
        
        state.state = BidState.calculate_state(bid, event_date)
        
        if not state.state in (BidState.CLOSED, BidState.PENDING) or not state.event_date:
            state.event_date = event_date 
        
        state.save()
        return state
   

class Bid(ProcessDeletedModel): 
    '''
    Заявка
    '''    
    client = models.ForeignKey(Client, verbose_name=_('Client'), related_name='bids', blank=True, null=True, on_delete=models.SET_NULL)
    clients = models.ManyToManyField(Client, verbose_name=_('Clients'), related_name='bids_m2m', blank=True, through='BidClient')
    estate_filter = PickledObjectField(blank=True, null=True)
    cleaned_filter = PickledObjectField(blank=True, null=True)
    history = models.OneToOneField(HistoryMeta, blank=True, null=True, editable=False)
    broker = models.ForeignKey(ExUser, verbose_name=_('User'), related_name='broker_list', blank=True, null=True, on_delete=models.PROTECT)
    brokers = models.ManyToManyField(ExUser, verbose_name=_('User'), blank=True)
    geo_groups = models.ManyToManyField(GeoGroup, verbose_name=_('GeoGroups'))    
    #Для поиска из пикле
    estates = models.ManyToManyField(Estate, verbose_name=_('Estate'), blank=True)    
    estate_categories = models.ManyToManyField(EstateTypeCategory, verbose_name=_('EstateTypeCategory'), blank=True)
    estate_types = models.ManyToManyField(EstateType, verbose_name=_('Estates types'), blank=True)
    regions = models.ManyToManyField(Region, verbose_name=_('Regions'), blank=True)
    localities = models.ManyToManyField(Locality, verbose_name=_('Locality'), blank=True)
    agency_price_min = models.IntegerField(verbose_name=_('Price min'), blank=True, null=True)
    agency_price_max = models.IntegerField(verbose_name=_('Price max'), blank=True, null=True)
    #Конец из пикле    
    note = models.TextField(_('Note'), blank=True, null=True)
    bid_status = models.ManyToManyField('BidStatus',verbose_name=_('BidStatus'),blank=True)       
    #attachments
    files = GenericRelation('EstateFile')
    @property
    def mixed_estate_types(self):
        result = []        
        cats_with_type = self.estate_types.values_list('estate_type_category_id', flat=True)
        cats_no_type = self.estate_categories.exclude(id__in=cats_with_type)
        result.extend(cats_no_type.values_list('types__name', flat=True).order_by('types__order'))
        result.extend(self.estate_types.values_list('name', flat=True).order_by('order'))
        return ', '.join(result)
    
    def update_state(self):
        return BidState.update_state(self)    
        
    @property
    def state_display(self):
        try:
            state = self.state
        except BidState.DoesNotExist:
            state = self.update_state()                    
        if state.is_expired:
            return u"просрочена"
        return state.get_state_display()   
        
    def get_state(self):
        try:
            state = self.state
        except BidState.DoesNotExist:
            state = self.update_state()       
        return state    
        
    def get_last_calendar_event(self):
        return self.bid_events.filter(bid_event_category__is_calendar=True).first()   
    
    def get_last_event(self):
        return self.bid_events.first()
    
    def is_closed(self):
        return self.has_status_category(BidStatusCategory.IRRELEVANT)
            
    def has_status_category(self, category):
        q = self.bid_status.filter(category=category)
        if q:
            return True
        return False
        
    def __unicode__(self):
        return u'%s' % self.pk                                  
    class Meta:      
        permissions = (
                ("view_other_bid", u'Просмотр чужих заявок'),
            )
        ordering = ['-history__created']
        verbose_name = _('Bid')
        verbose_name_plural = _('Bids')    

class BidStatusCategory(SimpleDict):
    '''
    Категория статусов заявки 
    '''
    IRRELEVANT = 3    
    class Meta(SimpleDict.Meta):
        verbose_name = _('Bid status category')
        verbose_name_plural = _('Bid status categories')

class BidStatus(SimpleDict):
    '''
    BidStatus    
    '''
    category = models.ForeignKey(BidStatusCategory,verbose_name=_('Category'), related_name='statuses', blank=True, null=True)
    class Meta(SimpleDict.Meta):
        verbose_name = _('Bid status')
        verbose_name_plural = _('Bid statuss')

class BidEventCategory(SimpleDict):
    '''
    Категория событий по заявке 
    '''    
    is_calendar = models.BooleanField(_('Calendar'), default=False)
    do_free = models.BooleanField(_('Free'), default=False)
    class Meta(SimpleDict.Meta):
        verbose_name = _('BidEventCategory')
        verbose_name_plural = _('BidEventCategories')

class BidEvent(models.Model):
    '''
    Событие по заявке 
    '''    
    bid = models.ForeignKey(Bid,verbose_name=_('Bid'), related_name='bid_events')
    bid_event_category = models.ForeignKey(BidEventCategory,verbose_name=_('BidEventCategory'))
    date = models.DateTimeField(verbose_name=_('Event date'), blank=True, null=True)
    estates = models.ManyToManyField(Estate, verbose_name=_('Estate'), blank=True)
    history = models.OneToOneField(HistoryMeta, blank=True, null=True, editable=False)
    note = models.TextField(_('Note'), blank=True, null=True)
    
    def __unicode__(self):
        return u'[%s] - %s' % (self.pk, self.bid_event_category)
    
    def is_free(self):
        return self.bid_event_category.do_free
    
    def as_dict(self):
        historical_color = '#cccccc'
        do_free_color = '#a09b7e'
        alert_color = '#fb5140'
        expired_color = '#c32515'
        result = {
            "id": self.id,
            "title": u'%s (%s)' % (self.bid_event_category.name, self.bid.pk),
            "start": self.date,
            #"end": self.date + datetime.timedelta(days=BidState.FREEDAYS),
            "url": reverse('bid_detail', args=[self.bid.pk]),
            "allDay": 'false'             
        }
        
        last_event = BidEvent.objects.filter(bid=self.bid).first()
        if last_event and last_event.bid_event_category.do_free:
            result['color'] = do_free_color
            result['description'] = u"последнее событие %s в заявке %s делает ее свободной" % (last_event, self.bid)
            return result
        
        if BidEvent.objects.filter(pk__gt=self.pk, bid=self.bid, bid_event_category__is_calendar=True):
            result['color'] = historical_color        
        else:
            days = (self.bid.state.event_date - datetime.datetime.now()).days
            if 0 < days < 2:
                result['color'] = alert_color
                result['description'] = u"заявка %s перейдет в свободные менее, чем через два дня" % self.bid
            elif self.bid.state.is_expired:
                result['color'] = expired_color  
        return result              
    
    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return
    
    class Meta:
        verbose_name = _('bid event')
        verbose_name_plural = _('bid events')        
        ordering = ['-date']

class RegisterCategory(SimpleDict):
    '''
    RegisterCategory
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Register category')
        verbose_name_plural = _('Register categorys')        

class EstateRegister(ProcessDeletedModel):
    '''
    Подборка
    '''    
    name = models.CharField(_('Name'), db_index=True, max_length=255)
    history = models.OneToOneField(HistoryMeta, blank=True, null=True, editable=False)    
    estates = models.ManyToManyField(Estate, verbose_name=_('Estate'), blank=True, related_name='estate_registers')    
    bids = models.ManyToManyField(Bid, verbose_name=_('EstateRegisters'), blank=True, related_name='estate_registers')
    register_category = models.ForeignKey(RegisterCategory,verbose_name=_('RegisterCategory'),blank=True,null=True)
    def __unicode__(self):
        return u'%s' % self.pk                          
    class Meta:      
        ordering = ['-id']
    @property
    def correct_estates(self):        
        return self.estates.filter(validity_id=Estate.VALID, history__modificated__gt = get_validity_delta())
         

class LocalityType(SimpleDict):
    '''
    LocalityType
    '''
    sort_name = models.CharField(_('Short name'), db_index=True, max_length=50) 
    prep_name = models.CharField(_('Prepositional Name'), db_index=True, max_length=255)
    class Meta(SimpleDict.Meta):
        verbose_name = _('LocalityType')
        verbose_name_plural = _('LocalityTypes')


class BidClient(models.Model):
    client = models.ForeignKey('Client')
    bid = models.ForeignKey('Bid')   
    class Meta:
        unique_together = ('client', 'bid')


class BuildingItem(models.Model):
    name = models.CharField(_('Name'), db_index=True, max_length=255)      
    yandex_building = models.ForeignKey('YandexBuilding', related_name='items', blank=True, null=True)
    room_count = models.PositiveIntegerField(_('Room count'), blank=True, null=True)
    total_area_min = models.DecimalField(_('Total area min'), blank=True, null=True, max_digits=10, decimal_places=2)
    total_area_max = models.DecimalField(_('Total area max'), blank=True, null=True, max_digits=10, decimal_places=2)
    used_area_min = models.DecimalField(_('Used area min'), blank=True, null=True, max_digits=10, decimal_places=2)
    used_area_max = models.DecimalField(_('Used area max'), blank=True, null=True, max_digits=10, decimal_places=2)
    price_per_sqm_min = models.IntegerField(verbose_name=_('Price min'), blank=True, null=True)
    price_per_sqm_max = models.IntegerField(verbose_name=_('Price max'), blank=True, null=True)
    def __unicode__(self):
        return u'%s' % self.name   
    class Meta(SimpleDict.Meta):
        verbose_name = _('BuildingItem')
        verbose_name_plural = _('BuildingItems')    
   
   
class YandexBuilding(models.Model):
    '''
    YandexBuilding
    '''       
    QUARTER_CHOICES = (
        (1, u'1-й квартал'),
        (2, u'2-й квартал'),        
        (3, u'3-й квартал'),
        (4, u'4-й квартал'),
    )
    STATE_CHOICES = (
        ('unfinished', u'строится'),
        ('built', u'дом построен, но не сдан'),        
        ('hand-over', u'сдан в эксплуатацию'),
    )    
    name = models.CharField(_('Name'), db_index=True, max_length=255)
    building_id = models.CharField(_('Yandex building id'), db_index=True, max_length=50, blank=True, null=True)
    cian_complex_id = models.CharField(u'ID ЖК в базе CIAN', max_length=50, blank=True, null=True) 
    ready_quarter = models.IntegerField(_('Quarter'), choices=QUARTER_CHOICES,) 
    ready_year = models.IntegerField(_('Ready year'), blank=True, null=True)
    building_state = models.CharField(_('Building state'), choices=STATE_CHOICES, max_length=15)
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'), blank=True, null=True)
    discount = models.TextField(verbose_name=_('Discount'), blank=True, null=True)
    dummy_address = models.CharField(_('Dummy address'), max_length=255, blank=True, null=True)
    
    wall_construcion = models.ForeignKey(WallConstrucion, verbose_name=_('Wall construcion'), blank=True, null=True, on_delete=models.PROTECT)
    exterior_finish = models.ForeignKey(ExteriorFinish, verbose_name=_('Exterior finish'), blank=True, null=True, on_delete=models.PROTECT)   
    wall_finish = models.ForeignKey(WallFinish, verbose_name=_('WallFinish'), blank=True, null=True, on_delete=models.PROTECT)
    price_per_sqm_min = models.IntegerField(verbose_name=_('Price per sq. m. min'), blank=True, null=True)
    price_per_sqm_max = models.IntegerField(verbose_name=_('Price per sq. m. max'), blank=True, null=True)
    
    supplies = GenericRelation('GenericSupply')
    files = GenericRelation('EstateFile')
    links = GenericRelation('GenericLink') 
    def __unicode__(self):
        return u'%s, %s' % (self.name, self.locality)   
    class Meta(SimpleDict.Meta):
        unique_together = ('name', 'locality')
        verbose_name = _('YandexBuilding')
        verbose_name_plural = _('YandexBuildings')    
        ordering = ['name']           
           

class DealStatus(SimpleDict):
    '''
    Статус сделки
    '''      
    class Meta(SimpleDict.Meta):
        verbose_name = _('DealStatus')
        verbose_name_plural = _('DealStatuses')
        
        
class GenericEvent(models.Model):
    '''
    Событие
    '''   
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')     
    category = models.ForeignKey(BidEventCategory, verbose_name=_('Category'))
    date = models.DateTimeField(verbose_name=_('Event date'), blank=True, null=True)    
    history = models.OneToOneField(HistoryMeta, blank=True, null=True, editable=False)
    note = models.TextField(_('Note'), blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=True) 
    
    def __unicode__(self):
        return u'[%s] - %s' % (self.pk, self.category)
           
    def is_last(self, filter_dict):
        last = GenericEvent.objects.filter(**filter_dict).first()
        return last.date <= self.date         
    
    def event_dict(self):
        result = {
                "id": self.id,
                "category": u'%s' % (self.category.name),
                "title": u'%s (%s)' % (self.category.name, self.content_object),
                "start": self.date,            
                "date": self.date.strftime('%d.%m.%y %H:%M'),
                "url": self.content_object.get_absolute_url(),
                "allDay": 'false',
                "deactivated": not self.is_active                
            }
        if self.note:
            result.update(
                {
                "note": self.note,
                "description": self.note,
                }
            )            
        if self.history:
            result.update({
                "modificated": naturaltime(self.history.modificated),
                "modificated_by": u'%s %s.' % (self.history.modificated_by.last_name, self.history.modificated_by.first_name[:1]),
                "history": u'Событие создано: %s %s.' % (self.history.created_by, self.history.created.strftime('%d.%m.%y %H:%M')),                                
                })
        return result
           
    def as_dict(self):
        return self.content_object.event_dict(self)             
    
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')        
        ordering = ['-date']         
   
   
from estatebase.signals import connect_signals
connect_signals()
