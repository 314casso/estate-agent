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
from settings import CORRECT_DELTA, INTEREST_RATE, MAX_CREDIT_MONTHS, \
    MAX_CREDIT_SUM
from estatebase.wrapper import get_wrapper, APARTMENT, NEWAPART, HOUSE, STEAD, \
    OUTBUILDINGS, AGRICULTURAL, FACILITIES, APARTMENTSTEAD, LANDSCAPING
import caching.base
from collections import OrderedDict
from django.template.base import Template
from django.utils.safestring import mark_safe
from django.template.context import Context
from django.utils.encoding import force_unicode



class ExUser(User):
    def __unicode__(self):
        return u'%s %s (%s)' % (self.first_name, self.last_name, self.username)
    class Meta:
        proxy = True

class UserProfile(models.Model):    
    user = models.OneToOneField(User)    
    geo_groups = models.ManyToManyField('GeoGroup', verbose_name=_('Geo group'),)
    office = models.ForeignKey('Office', blank=True, null=True, verbose_name=_('Office'), on_delete=models.PROTECT)                

class SimpleDict(caching.base.CachingMixin, models.Model):
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
    geo_group = models.ForeignKey(GeoGroup, verbose_name=_('GeoGroup'), on_delete=models.PROTECT)
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
    class Meta(SimpleDict.Meta):
        verbose_name = _('Office')
        verbose_name_plural = _('Offices')

class Locality(models.Model):
    '''
    Населенный пункт
    '''
    name = models.CharField(_('Name'), db_index=True, max_length=255)
    region = models.ForeignKey(Region, blank=True, null=True, verbose_name=_('Region'), on_delete=models.PROTECT)
    def __unicode__(self):
        return u'%s' % self.name
    def natural_key(self):
        return self.__unicode__()
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
    name = models.CharField(_('Name'), db_index=True, max_length=255)
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'), on_delete=models.PROTECT)
    def __unicode__(self):
        return u'%s' % self.name
    def natural_key(self):
        return self.__unicode__()
    class Meta:
        verbose_name = _('street')
        verbose_name_plural = _('streets')
        unique_together = ('name', 'locality')
        ordering = ['name']

class Beside(SimpleDict):    
    '''
    Рассояние до (моря, речки и т.п.)
    '''
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
    name = models.CharField(_('Name'), max_length=100)
    independent = models.BooleanField(_('Independent'), default=True)
    has_bidg = models.IntegerField(_('HasBidg'), choices=AVAILABILITY_CHOICES)
    has_stead = models.IntegerField(_('HasStead'), choices=AVAILABILITY_CHOICES)
    is_commerce = models.BooleanField(_('Commerce'), default=False)
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
        )    
    name = models.CharField(_('Name'), max_length=100)
    estate_type_category = models.ForeignKey(EstateTypeCategory, verbose_name=_('EstateTypeCategory'), on_delete=models.PROTECT, related_name='types')   
    template = models.IntegerField(_('Template'), choices=TEMPLATE_CHOICES)
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255)
    placeable = models.BooleanField(_('Placeable'), default=True)        
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
    def get_query_set(self):
        return super(BaseModelManager, self).get_query_set().filter(deleted=False)

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
    
class Estate(ProcessDeletedModel):
    '''
    Базовая модель объектов недвижимости
    '''
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
    #Базовые
    estate_category = models.ForeignKey(EstateTypeCategory, verbose_name=_('EstateCategory'), on_delete=models.PROTECT)
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.PROTECT) 
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'), on_delete=models.PROTECT, blank=True, null=True)
    microdistrict = models.ForeignKey('Microdistrict', verbose_name=_('Microdistrict'), blank=True, null=True, on_delete=models.PROTECT)
    street = models.ForeignKey(Street, verbose_name=_('Street'), on_delete=models.PROTECT, blank=True, null=True)    
    estate_number = models.CharField(_('Estate number'), max_length=10, blank=True, null=True)
    clients = models.ManyToManyField('Client', verbose_name=_('Clients'), related_name='estates', through=EstateClient)
    origin = models.ForeignKey('Origin', verbose_name=_('Origin'), blank=True, null=True, on_delete=models.PROTECT)
    beside = models.ForeignKey('Beside', verbose_name=_('Beside'), blank=True, null=True, on_delete=models.PROTECT)
    beside_distance = models.PositiveIntegerField(_('Beside distance'), blank=True, null=True)
    saler_price = models.PositiveIntegerField(_('Saler price'), blank=True, null=True)
    agency_price = models.PositiveIntegerField(_('Agency price'), blank=True, null=True)
    estate_status = models.ForeignKey('EstateStatus', verbose_name=_('Estate status'), on_delete=models.PROTECT)
    com_status = models.ForeignKey(ComStatus, verbose_name=_('ComStatus'), blank=True, null=True)         
    #Коммуникации    
    electricity = models.ForeignKey('Electricity', verbose_name=_('Electricity'), blank=True, null=True, on_delete=models.PROTECT)
    electricity_distance = models.PositiveIntegerField('Electricity distance', blank=True, null=True)
    watersupply = models.ForeignKey('Watersupply', verbose_name=_('Watersupply'), blank=True, null=True, on_delete=models.PROTECT) 
    watersupply_distance = models.PositiveIntegerField(_('Watersupply distance'), blank=True, null=True)
    gassupply = models.ForeignKey('Gassupply', verbose_name=_('Gassupply'), blank=True, null=True, on_delete=models.PROTECT)
    gassupply_distance = models.PositiveIntegerField(_('Gassupply distance'), blank=True, null=True)
    sewerage = models.ForeignKey('Sewerage', verbose_name=_('Sewerage'), blank=True, null=True, on_delete=models.PROTECT)
    sewerage_distance = models.PositiveIntegerField(_('Sewerage distance'), blank=True, null=True)
    telephony = models.ForeignKey('Telephony', verbose_name=_('Telephony'), blank=True, null=True, on_delete=models.PROTECT)
    internet = models.ForeignKey('Internet', verbose_name=_('Internet'), blank=True, null=True, on_delete=models.PROTECT)
    driveway = models.ForeignKey('Driveway', verbose_name=_('Driveway'), blank=True, null=True, on_delete=models.PROTECT)
    driveway_distance = models.PositiveIntegerField(_('Driveway distance'), blank=True, null=True)
    #Дополнительно    
    estate_params = models.ManyToManyField(EstateParam, verbose_name=_('Estate params'), blank=True, null=True)    
    description = models.TextField(_('Description'), blank=True, null=True)
    client_description = models.TextField(_('Client description'), blank=True, null=True)
    comment = models.TextField (_('Comment'), blank=True, null=True, max_length=255)  
    #Изменения
    history = models.OneToOneField(HistoryMeta, blank=True, null=True)
    contact = models.ForeignKey('Contact', verbose_name=_('Contact'), blank=True, null=True, on_delete=models.PROTECT)  
    validity = models.ForeignKey(Validity, verbose_name=_('Validity'), blank=True, null=True)
    broker = models.ForeignKey(ExUser, verbose_name=_('Broker'), blank=True, null=True, on_delete=models.PROTECT)
    def check_contact(self):
        return self.contact and self.contact.contact_state_id == Contact.AVAILABLE
    def check_validity(self):
        report = OrderedDict([(self.NOTFREE, False), (self.NOCONACT, False), (self.DRAFT, [])])
        report[self.NOCONACT] = not self.check_contact() 
        if not self.estate_status_id == self.FREE:
            report[self.NOTFREE] = True    
        if not self.street and not (self.basic_stead and self.basic_stead.estate_type.template == AGRICULTURAL):
            report[self.DRAFT].append(unicode(_('Street')))
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
            if not self.basic_bidg.floor and not self.basic_bidg.estate_type.template in (HOUSE, OUTBUILDINGS):                                
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
        if self.basic_stead:
            if not self.basic_stead.total_area:
                report[self.DRAFT].append(u'Площадь участка')        
        return report
    
    def set_validity(self, report):
        self.validity_id = self.VALID        
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
        if not self.correct and self.validity == self.VALID:
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
        #bidgs = list(self.bidgs.all()[:1])
        if bidgs:
            return bidgs[0]                                  
    @property
    def basic_stead(self):        
        try:
            return self.stead
        except Stead.DoesNotExist:
            return None    
    @property
    def correct(self):
        return self.validity_id == self.VALID and (self.history.modificated > CORRECT_DELTA)
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
        if self.estate_category.is_stead:
            return self.stead.estate_type.name
        else:
            result = []
            for bidg in self.bidgs.all():
                if bidg.estate_type.estate_type_category.independent:
                    result.append(bidg.estate_type.name)
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
            
    class Meta:
        verbose_name = _('estate')
        verbose_name_plural = _('estate')
        ordering = ['-id']    
        permissions = (
            ("view_private", u'Просмотр цены, полного адреса и контактов'),
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
    documents = models.ManyToManyField(Document, verbose_name=_('Documents'), blank=True, null=True)
    #Внутренняя отделка    
    wall_finish = models.ForeignKey(WallFinish, verbose_name=_('WallFinish'), blank=True, null=True, on_delete=models.PROTECT)
    flooring = models.ForeignKey(Flooring, verbose_name=_('Flooring'), blank=True, null=True, on_delete=models.PROTECT)
    ceiling = models.ForeignKey(Ceiling, verbose_name=_('Ceiling'), blank=True, null=True, on_delete=models.PROTECT)
    interior = models.ForeignKey(Interior, verbose_name=_('Interior'), blank=True, null=True, on_delete=models.PROTECT)
    appliances = models.ManyToManyField(Appliance,verbose_name=_('Appliance'),blank=True,null=True)
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
    def is_facility(self):
        return self.estate_type.template in [FACILITIES, LANDSCAPING]
    @property
    def is_independent(self):
        return self.estate_type.estate_type_category.independent
    def __unicode__(self):
        return u'%s' % self.pk
           
    
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
    documents = models.ManyToManyField(Document, verbose_name=_('Documents'), blank=True, null=True)    
    class Meta:
        verbose_name = _('stead')
        verbose_name_plural = _('steads')
    @property
    def field_list(self):
        wrapper = get_wrapper(self)                          
        return wrapper.field_list()
    @property
    def total_area_sotka(self):
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
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255) 
    history = models.OneToOneField(HistoryMeta, blank=True, null=True, editable=False)    
    def __unicode__(self):
        return u'%s: %s' % (self.name, ', '.join(self.contacts.all().values_list('contact', flat=True)))    
    @property
    def user(self):
        return self.history.updated_by or self.history.created_by                
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
    event_date = models.DateTimeField(_('Event Date'), default=datetime.datetime.now())
    user = models.ForeignKey(ExUser, verbose_name=_('User'), blank=True, null=True, on_delete=models.PROTECT)
    contact_state = models.ForeignKey(ContactState, verbose_name=_('Contact State'), on_delete=models.PROTECT) 
    contact = models.ForeignKey('Contact', verbose_name=_('Contact'),)
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
    contact = models.CharField(_('Contact'), max_length=255, db_index=True)
    updated = models.DateTimeField(_('Updated'), blank=True, null=True)   
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
        q = Contact.objects.filter(contact__iexact=self.contact)
        if self.id:
            q = q.exclude(pk=self.id)
        if q.count() > 0:
            client = list(q.all()[:1])[0].client
            extra = ''
            t = None
            if not client.deleted:
                t = Template(u'<a title="Показать карточку клиента в оттельном окне..." target="_blank" href="{% url client_detail pk %}">[{{ pk }}] {{ name }}</a>')
                t = t.render(Context({ 'name': client.name, 'pk': client.pk }))
            else:
                t = '"[%s] %s"' % (client.pk, client.name)                
                extra = u' - находится в корзине! %s'
                restore = Template(u'<a target="_blank" href="{% url client_restore pk %}">Восстановить</a>')
                extra = extra % restore.render(Context({ 'pk': client.pk }))
            raise ValidationError(mark_safe(u'Данный контакт уже создан и принадлежит %s %s' % (t, extra)))
                     
        if not self.contact_type_id:
            raise ValidationError(u'Вид контакта не может оставаться пустым!')
        validate_url = URLValidator(verify_exists=False)
        validate_phone = RegexValidator(regex=r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')        
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

class Bid(ProcessDeletedModel):
    '''
    Заявка
    '''      
    client = models.ForeignKey(Client, verbose_name=_('Client'), related_name='bids')
    estate_filter = PickledObjectField(blank=True, null=True)
    cleaned_filter = PickledObjectField(blank=True, null=True)
    history = models.OneToOneField(HistoryMeta, blank=True, null=True, editable=False)
    broker = models.ForeignKey(ExUser, verbose_name=_('User'), related_name='broker_list', blank=True, null=True, on_delete=models.PROTECT)
    brokers = models.ManyToManyField (ExUser, verbose_name=_('User'), blank=True, null=True)
    #Для поиска из пикле
    estates = models.ManyToManyField(Estate, verbose_name=_('Estate'), blank=True, null=True)    
    estate_categories = models.ManyToManyField(EstateTypeCategory, verbose_name=_('EstateTypeCategory'), blank=True, null=True)
    estate_types = models.ManyToManyField(EstateType, verbose_name=_('Estates types'), blank=True, null=True)
    regions = models.ManyToManyField(Region, verbose_name=_('Regions'), blank=True, null=True)
    localities = models.ManyToManyField(Locality, verbose_name=_('Locality'), blank=True, null=True)
    agency_price_min = models.IntegerField(verbose_name=_('Price min'), blank=True, null=True)
    agency_price_max = models.IntegerField(verbose_name=_('Price max'), blank=True, null=True)
    #Конец из пикле    
    note = models.TextField(_('Note'), blank=True, null=True)
    bid_status = models.ManyToManyField('BidStatus',verbose_name=_('BidStatus'),blank=True,null=True)
    @property
    def mixed_estate_types(self):
        result = []        
        cats_with_type = self.estate_types.values_list('estate_type_category_id', flat=True)
        cats_no_type = self.estate_categories.exclude(id__in=cats_with_type)
        result.extend(cats_no_type.values_list('types__name', flat=True).order_by('types__order'))
        result.extend(self.estate_types.values_list('name', flat=True).order_by('order'))
        return ', '.join(result)
        
        
    def __unicode__(self):
        return u'%s' % self.pk                                  
    class Meta:      
        ordering = ['-history__created']    

class BidStatus(SimpleDict):
    '''
    BidStatus
    ./manage.py loaddata bidstatus.json
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('Bid status')
        verbose_name_plural = _('Bid statuss')

class BidEventCategory(SimpleDict):
    '''
    Категория событий по заявке 
    '''
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
    estates = models.ManyToManyField(Estate, verbose_name=_('Estate'), blank=True, null=True)
    history = models.OneToOneField(HistoryMeta, blank=True, null=True, editable=False)
    note = models.TextField(_('Note'), blank=True, null=True)
    def __unicode__(self):
        return u'[%s] - %s' % (self.pk, self.bid_event_category)
    class Meta:
        verbose_name = _('bid event')
        verbose_name_plural = _('bid events')        

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
    estates = models.ManyToManyField(Estate, verbose_name=_('Estate'), blank=True, null=True, related_name='estate_registers')    
    bids = models.ManyToManyField(Bid, verbose_name=_('EstateRegisters'), blank=True, null=True, related_name='estate_registers')
    register_category = models.ForeignKey(RegisterCategory,verbose_name=_('RegisterCategory'),blank=True,null=True)
    def __unicode__(self):
        return u'%s' % self.pk                          
    class Meta:      
        ordering = ['-id']
   
from estatebase.signals import connect_signals
connect_signals()
