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
    '''
    Районы
    '''
    class Meta(SimpleDict.Meta):
        verbose_name = _('region')
        verbose_name_plural = _('regions')

class Locality(SimpleDict):
    '''
    Населенные пункты
    '''
    region = models.ForeignKey(Region, blank=True, null=True, verbose_name=_('Region'),)
    class Meta(SimpleDict.Meta):
        verbose_name = _('locality')
        verbose_name_plural = _('localities')    

class Microdistrict(SimpleDict):
    '''
    Микрорайоны в населенном пункте
    '''
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'),)
    class Meta(SimpleDict.Meta):
        verbose_name = _('microdistrict')
        verbose_name_plural = _('microdistricts')

class Street(SimpleDict):
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'),)
    class Meta(SimpleDict.Meta):
        verbose_name = _('street')
        verbose_name_plural = _('streets')

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
    estate_type = models.ManyToManyField('EstateType', verbose_name=_('EstateType'),)
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

VIEW_PREFIX_CHOICES = (
    ('apartment','Квартира'),
)

class EstateType(OrderedModel):
    name = models.CharField(_('Name'), max_length=100)
    estate_type_category = models.ForeignKey(EstateTypeCategory, verbose_name=_('EstateTypeCategory'),)    
    object_type = models.CharField(_('Object type'), max_length=50, choices=OBJECT_TYPE_CHOICES)
    view_prefix = models.CharField(_('View prefix'), max_length=50, choices=VIEW_PREFIX_CHOICES)
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
    
class HistoryMeta(models.Model):
    created = models.DateTimeField(_('Created'),)
    created_by = models.ForeignKey(ExUser, verbose_name=_('User'), related_name='creators' )
    updated = models.DateTimeField(_('Updated'), blank=True, null=True)
    updated_by = models.ForeignKey(ExUser, verbose_name=_('Updated by'), blank=True, null=True, related_name='updators')                        
    
def prepare_history(history,user):
    if not history:
        history = HistoryMeta()        
        history.created = datetime.datetime.now()
        history.created_by = user
        history.save() 
    elif user:
        history.updated = datetime.datetime.now()
        history.updated_by = user
        history.save()
    return history                 
    
class Estate(models.Model):
    '''
    Базовая модель объектов недвижимости
    '''
    #Базовые
    estate_type = models.ForeignKey(EstateType, verbose_name=_('EstateType'),)
    region = models.ForeignKey(Region, blank=True, null=True, verbose_name=_('Region'),) 
    locality = models.ForeignKey(Locality, verbose_name=_('Locality'),)
    microdistrict = models.ForeignKey('Microdistrict', verbose_name=_('Microdistrict'), blank=True, null=True)
    street = models.ForeignKey(Street, verbose_name=_('Street'),)    
    estate_number = models.CharField(_('Estate number'), max_length=10)
    clients = models.ManyToManyField('Client', verbose_name=_('Clients'),related_name='estates')
    origin = models.ForeignKey('Origin', verbose_name=_('Origin'), blank=True, null=True)
    beside = models.ForeignKey('Beside', verbose_name=_('Beside'), blank=True, null=True)
    beside_distance = models.PositiveIntegerField('Beside distance',blank=True, null=True)
    saler_price = models.PositiveIntegerField('Saler price',blank=True, null=True)
    agency_price = models.PositiveIntegerField('Agency price', blank=True, null=True)
    estate_status = models.ForeignKey('EstateStatus', verbose_name=_('Estate status'))     
    #Коммуникации    
    electricity = models.ForeignKey('Electricity', verbose_name=_('Electricity'), blank=True, null=True)
    electricity_distance = models.PositiveIntegerField('Electricity distance',blank=True, null=True)
    watersupply = models.ForeignKey('Watersupply', verbose_name=_('Watersupply'), blank=True, null=True) 
    watersupply_distance = models.PositiveIntegerField('Watersupply distance',blank=True, null=True)
    gassupply = models.ForeignKey('Gassupply', verbose_name=_('Gassupply'), blank=True, null=True)
    gassupply_distance = models.PositiveIntegerField('Gassupply distance',blank=True, null=True)
    sewerage = models.ForeignKey('Sewerage', verbose_name=_('Sewerage'), blank=True, null=True)
    sewerage_distance = models.PositiveIntegerField('Sewerage distance',blank=True, null=True)
    telephony = models.ForeignKey('Telephony', verbose_name=_('Telephony'), blank=True, null=True)
    internet = models.ForeignKey('Internet', verbose_name=_('Internet'), blank=True, null=True)
    driveway = models.ForeignKey('Driveway', verbose_name=_('Driveway'), blank=True, null=True)
    driveway_distance = models.PositiveIntegerField('Driveway distance',blank=True, null=True)
    #Дополнительно
    documents = models.ManyToManyField(Document, verbose_name=_('Documents'), blank=True, null=True)
    estate_params = models.ManyToManyField(EstateParam, verbose_name=_('Estate params'), blank=True, null=True)    
    description = models.TextField(_('Description'), blank=True, null=True)
    comment = models.TextField (_('Note'), blank=True, null=True, max_length=255)  
    #Изменения
    history = models.OneToOneField(HistoryMeta,blank=True, null=True)  
    @property
    def is_bidg(self):
        if self.estate_type.object_type  == 'BIDG':
            return True
    @property
    def basic_bidg(self):
        if self.bidgs:
            bidgs = list(self.bidgs.all()[:1])
            if bidgs:
                return bidgs[0]                      
    class Meta:
        verbose_name = _('estate')
        verbose_name_plural = _('estate')
    
    def __unicode__(self):
        return u'%s' % self.pk
    
    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)                        
        self.history = prepare_history(self.history,user)                                                     
        super(Estate, self).save(*args, **kwargs)                

class Bidg(models.Model):
    estate = models.ForeignKey(Estate, verbose_name=_('Estate'), related_name='bidgs')   
    room_number = models.CharField(_('Bidg number'), max_length=10, blank=True, null=True)
    year_built = models.PositiveIntegerField(_('Year built'), blank=True, null=True)
    floor = models.PositiveIntegerField(_('Floor'), blank=True, null=True)
    elevator = models.BooleanField(_('Elevator'), default=False)
    #wall_construcion = 
    #exterior_finish =
    #window_type =
    #heating =
    #ceiling_height = 
    room_count = models.PositiveIntegerField(_('Room count'), blank=True, null=True)
    total_area = models.DecimalField(_('Total area'), blank=True, null=True, max_digits=7, decimal_places=2)
    used_area = models.DecimalField(_('Used area'), blank=True, null=True, max_digits=7, decimal_places=2)
    class Meta:
        verbose_name = _('bidg')
        verbose_name_plural = _('bidgs')

class Steed(models.Model):
    estate = models.OneToOneField(Estate, verbose_name=_('Estate'), related_name='steed')    
    class Meta:
        verbose_name = _('steed')
        verbose_name_plural = _('steeds')

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

class Client(models.Model):
    """
    An client entity      
    """
    name = models.CharField(_('Name'), max_length=255)
    client_type = models.ForeignKey(ClientType, verbose_name=_('ClientType'),)
    origin = models.ForeignKey(Origin, verbose_name=_('Origin'), blank=True, null=True) 
    address = models.CharField(_('Address'), blank=True, null=True, max_length=255)
    note = models.CharField(_('Note'), blank=True, null=True, max_length=255) 
    history = models.OneToOneField(HistoryMeta,blank=True, null=True, editable=False)         
    def __unicode__(self):
        return u'%s %s' % (self.name, self.address)
    @property
    def contacts(self):
        return self.contactlist.all().select_related('contact_type')
    @property
    def user(self):
        return self.history.updated_by or self.history.created_by 
    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)                                           
        self.history = prepare_history(self.history,user)                                     
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


    
