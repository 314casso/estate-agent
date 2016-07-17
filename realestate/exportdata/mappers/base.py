# -*- coding: utf-8 -*-
from estatebase.models import EstateTypeCategory, EstateType, Locality
from exportdata.models import ValueMapper
import re
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
import hashlib

def number2xml(d):
    return '%.12g' % d if d else ''

class BaseMapper(object):    
    def __init__(self, estate, feed):
        self._estate = estate
        self._basic_bidg = estate.basic_bidg
        self._basic_bidg = self._estate.basic_bidg        
        self._layout = None
        self._price = self.Price(estate)      
        self._address = self.Address(estate)
        self._contact = self.Contact(estate, feed.campaign)
        self._feed = feed
    
    class Contact:
        _office = None
        
        def __init__(self, estate, campaign):
            self._campaign = campaign
            self._estate = estate           
        
        @property
        def office(self):
            if not self._office:
                self._office = self._estate.region.office_set.all()[:1].get()
            return self._office
    
        @property
        def manager_name(self):    
            if self._campaign and self._campaign.valid and self._campaign.person:
                return u'%s' % self._campaign.person     
            return u'%s' % self.office.head.first_name
    
        @property
        def email(self):    
            if self._campaign and self._campaign.valid and self._campaign.email:
                return u'%s' % self._campaign.email     
            return u'%s' % self._office.head.email
         
        @property
        def phone(self):    
            if self._campaign and self._campaign.valid and self._campaign.phone:
                return u'%s' % self._campaign.phone     
            return u'%s' % self._office.head.userprofile.phone
    
    @staticmethod
    def get_value_mapper(model_class, object_id, xml_node):
        cache_key = hashlib.md5(("%s%s%s" % (model_class, object_id, xml_node))).hexdigest()                                               
        xml_value = cache.get(cache_key)
        if xml_value is not None:            
            return xml_value
        try:
            value_mapper = ValueMapper.objects.get(content_type=ContentType.objects.get_for_model(model_class), object_id=object_id, mapped_node__xml_node=xml_node)
            xml_value = value_mapper.xml_value
            cache.set(cache_key, xml_value, 300)
            return xml_value             
        except ValueMapper.DoesNotExist:
            return
    
    @property
    def rooms(self):
        if self._basic_bidg:
            return number2xml(self._basic_bidg.room_count)
            
    @property
    def price(self):
        return self._price
    
    @property
    def contact(self):
        return self._contact
    
    @property
    def address(self):
        return self._address
    
    class Address:      
        _city = None  
        _district = None    
        _street = None
        _bld_number = None
        
        def __init__(self, estate):
            self._estate = estate
                
        @property
        def locality(self):
            if not self._city:
                self._city = u'%s %s' % (self._estate.locality.name, self._estate.locality.locality_type.sort_name)
            return self._city
        
        @property    
        def district(self):
            if not self._district:
                self._district = self._estate.region.regular_name
            return self._district
            
        @property
        def street(self):
            if not self._estate.street:
                return ''
            if not self._street:
                self._street = u'%s %s' % (self._estate.street.name, self._estate.street.street_type or '')
            return self._street
        
        @property
        def bld_number(self):
            if not self._bld_number:
                self._bld_number = self._estate.estate_number
            return self._bld_number
        
        @property    
        def country(self):
            return u'Россия'
        
        @property
        def region(self):
            return u'Краснодарский край'
    
    class Price:
        def __init__(self, estate):
            self._estate = estate     
        def value(self):
            return re.sub(r'\s', '', str(self._estate.agency_price))       
    
        

class AvitoMapper(BaseMapper):    
    _id = None
    _category = None
    
    @property    
    def id(self):
        if not self._id:
            self._id = self.get_id()           
        return self._id 
        
    @property
    def category(self):
        if not self._category:
            self._category = self.get_category()
        return self._category

    def get_id(self):
        return str(self._estate.id)
    
    def get_category(self):
        cat_id = self._estate.estate_category_id
        if cat_id == EstateTypeCategory.KVARTIRA and self._basic_bidg is not None:
            type_id = self._basic_bidg.estate_type_id                                            
            category = BaseMapper.get_value_mapper(EstateType, type_id, 'ObjectType')
            if category:
                return category             
        return BaseMapper.get_value_mapper(EstateTypeCategory, cat_id, 'Category')
                     
    class Price(BaseMapper.Price):
        def type(self):
            return u'за всё'
    
    class Address(BaseMapper.Address):    
        @property
        def city(self):
            if not self._city:
                self._city = BaseMapper.get_value_mapper(Locality, self._estate.locality_id, 'City')
            return self._city
    
#     
#     def distance_to_city(self):
#         if self._estate.estate_category_id in (EstateTypeCategory.KVARTIRA, EstateTypeCategory.COMMERCE):
#             return
#         return u'0'
#         
#     def sale_rooms(self):
#         if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:
#             self.rooms()
#     
#     def object_type(self):
#         if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:
#             return        
#         if self._estate.estate_category_id in (EstateTypeCategory.DOM, EstateTypeCategory.KVARTIRAU4ASTOK):             
#             type_mapper = {
#                            EstateTypeMapper.DACHA:u'Дача',
#                            EstateTypeMapper.DOM:u'Дом',
#                            EstateTypeMapper.POLDOMA:u'Таунхаус',
#                            EstateTypeMapper.KVARTIRASUCHASTKOM:u'Таунхаус',
#                            EstateTypeMapper.KOTTEDZH:u'Коттедж',
#                            EstateTypeMapper.TAUNHAUS:u'Таунхаус',
#                            EstateTypeMapper.DUPLEKS:u'Таунхаус',                       
#                            }
#             return type_mapper.get(self._basic_bidg.estate_type_id) 
#         if self._estate.estate_category_id == EstateTypeCategory.U4ASTOK:
#             type_mapper = {
#                            EstateTypeMapper.DACHNYYUCHASTOK :u'Сельхозназначения (СНТ, ДНП)',
#                            EstateTypeMapper.UCHASTOKDLYASTROITELSTVADOMA:u'Поселений (ИЖС)',
#                            EstateTypeMapper.UCHASTOKSELSKOHOZYAYSTVENNOGONAZNACHENIYA:u'Сельхозназначения (СНТ, ДНП)',
#                            EstateTypeMapper.UCHASTOKKOMMERCHESKOGONAZNACHENIYA:u'Промназначения',
#                            EstateTypeMapper.UCHASTOKINOGONAZNACHENIYA:u'Промназначения',                                                  
#                            }
#             return type_mapper.get(self._basic_stead.estate_type_id)
#         if self._estate.estate_category_id == EstateTypeCategory.COMMERCE:
#             DEFAULT = u'Помещение свободного назначения';
#             estate_type_id = None
#             if self._basic_bidg:
#                 estate_type_id = self._basic_bidg.estate_type_id
#             elif self._basic_stead:
#                 estate_type_id = self._basic_stead.estate_type_id
#             type_mapper = {
#                            EstateTypeMapper.ADMINISTRATIVNOTORGOVOEZDANIE :u'Торговое помещение',                                                                            
#                            EstateTypeMapper.TORGOVYYPAVILON :u'Торговое помещение',
#                            EstateTypeMapper.MAGAZIN :u'Торговое помещение',
#                            EstateTypeMapper.GOSTINITSA :u'Гостиница',
#                            EstateTypeMapper.GOSTEVOYDOM :u'Гостиница',
#                            EstateTypeMapper.GOSTEVYEKOMNATY :u'Гостиница',
#                            EstateTypeMapper.GOSTINICHNYYKOMPLEKS :u'Гостиница',
#                            EstateTypeMapper.PANSIONAT :u'Гостиница',
#                            EstateTypeMapper.OTEL :u'Гостиница',
#                            EstateTypeMapper.MINIGOSTINITSA :u'Гостиница',
#                            EstateTypeMapper.SANATORIY :u'Гостиница',
#                            EstateTypeMapper.OFIS :u'Офисное помещение',
#                            EstateTypeMapper.ADMINISTRATIVNOEZDANIE :u'Офисное помещение',
#                            EstateTypeMapper.RESTORAN :u'Ресторан, кафе',
#                            EstateTypeMapper.KAFE :u'Ресторан, кафе',
#                            EstateTypeMapper.SALONKRASOTY :u'Салон красоты',
#                            EstateTypeMapper.SKLAD :u'Складское помещение',
#                            EstateTypeMapper.PROIZVODSTVENNOSKLADSKAYABAZA :u'Складское помещение',                           
#                            }
#             return type_mapper.get(estate_type_id, DEFAULT)
#             
#     def feed_locality(self, feed_name):
#         result = {}
#         try:
#             feed_locality = FeedLocality.objects.get(feed_name=feed_name, locality=self._estate.locality)
#             result['city'] = feed_locality.locality.name
#             return result            
#         except FeedLocality.DoesNotExist:
#             result['city'] = self._estate.locality.region.metropolis.name
#             result['locality'] = self._estate.locality.name
#             return result
#     
#     def ad_status(self):
#         return u'Free'             
#      
    @property
    def operation_type(self):        
        return u'Продам'
    
    @property
    def ad_status(self):
        return u'Free'
        
    @property
    def allow_email(self):
        return u'Да'
       
    
#     
#     def living_space(self):
#         used_area = self._basic_bidg.used_area
#         if used_area:
#             return number2xml(used_area)        
#         return number2xml(round(random.uniform(0.55, 0.62) * round(self._basic_bidg.total_area), 1))
#             
#     def new_flat(self):
#         new_flat = super(AvitoWrapper,self).new_flat()        
#         return u'Новостройка' if new_flat else u'Вторичка'
#     
#     def format_int_result(self, value, if_none='0'):
#         return number2xml(value) if value else if_none
#     
#     def house_type(self):
#         if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:    
#             mapper = { 
#                       WallConstrucionMapper.PANEL: u'Панельный', WallConstrucionMapper.KIRPICH: u'Кирпичный', 
#                       WallConstrucionMapper.MONOLIT: u'Монолитный', WallConstrucionMapper.BLOK: u'Блочный',
#                       WallConstrucionMapper.DEREVO: u'Деревянный'
#                      }        
#             wall_construcion_id = self._basic_bidg.wall_construcion_id
#             if wall_construcion_id in mapper:
#                 return mapper.get(wall_construcion_id)        
#             
#     def walls_type(self):
#         if not self._estate.estate_category_id == EstateTypeCategory.KVARTIRA and self._basic_bidg:    
#             mapper = { 
#                       WallConstrucionMapper.PANEL: u'Ж/б панели', WallConstrucionMapper.KIRPICH: u'Кирпич', 
#                       WallConstrucionMapper.PENOBLOK: u'Пеноблоки', WallConstrucionMapper.PENOBETON:u'Пеноблоки', 
#                       WallConstrucionMapper.DEREVO: u'Бревно', WallConstrucionMapper.BRUS:u'Брус', 
#                       WallConstrucionMapper.METALL:u'Металл', WallConstrucionMapper.BLOK:u'Пеноблоки', 
#                      }        
#             wall_construcion_id = self._basic_bidg.wall_construcion_id
#             if wall_construcion_id in mapper:
#                 return mapper.get(wall_construcion_id)
#     
#     def locality(self):
#         GOROD = 1
#         pref = []
#         if self._estate.locality.locality_type_id != GOROD:             
#             pref.append(self._estate.locality.region.regular_name)
#             locality_type = self._estate.locality.locality_type.name.lower()
#             pref.append(locality_type)
#         if pref:
#             pref_str = u', '.join(pref)
#             return u'%s %s' % (pref_str, self._estate.locality.name)   
#         return self._estate.locality.name
#     
#     def street(self):
#         if self._estate.street:
#             return u'%s %s' % (self._estate.street.street_type or '', self._estate.street.name)