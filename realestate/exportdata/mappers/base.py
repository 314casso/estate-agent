# -*- coding: utf-8 -*-
from estatebase.models import EstateTypeCategory, EstateType, Locality,\
    WallConstrucion
from exportdata.models import ValueMapper
import re
from django.core.cache import cache
from django.template import loader
from django.template.context import Context
from django.template.defaultfilters import striptags
from django.contrib.contenttypes.models import ContentType
import hashlib
import os
import logging
from django.utils.encoding import smart_unicode

logger = logging.getLogger('estate')

def number2xml(d):
    return '%.12g' % d if d else ''

class BaseMapper(object):
    _description = None  
    _living_space = None  
    _area = None
    _land_area = None
    _floor = None
    _floors = None
    
    def __init__(self, estate, feed):
        self._estate = estate
        self._basic_bidg = estate.basic_bidg
        self._basic_stead = self._estate.basic_stead                
        self._layout = None
        self._price = self.Price(estate)      
        self._address = self.Address(estate)
        self._contact = self.Contact(estate, feed.campaign)
        self._feed = feed
        self._domain = 'http://%s' % 'feed.domnatamani.ru' 
    
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
            return smart_unicode(xml_value)
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
        _distance_to_city = None 
        
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
        def distance_to_city(self):
            if not self._distance_to_city:
                self._distance_to_city = u'0'
            return self._distance_to_city
        
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
        
    def render_content(self, estate, description, short=False):        
        t = loader.get_template('reports/feed/text_content.html')
        c = Context({'estate_item':estate, 'description': description, 'short': short})
        rendered = t.render(c)
        return re.sub(r"\s+"," ", rendered).strip()
    
    def render_post_description(self, estate):
        region = u'Краснодарского края' if estate.locality.locality_type_id == Locality.CITY else estate.locality.region.regular_name_gent
        location = u'%s %s' % (estate.locality.name_loct, region)
        result = u'Продается %s в %s' % (estate.estate_type.lower(), location)             
        return result
    
    @property        
    def description(self):
        if not self._description:
            description = self.render_post_description(self._estate)        
            return striptags(self.render_content(self._estate, description))
        return self._description
    
    @property
    def living_space(self):
        # жилая площадь (при продаже комнаты — площадь комнаты)
        if not self._living_space:
            if self._basic_bidg:             
                self._living_space = number2xml(self._basic_bidg.used_area)            
        return self._living_space       
    
    @property
    def area(self):
        # общая площадь
        if not self._area:
            if self._basic_bidg:             
                self._area = number2xml(self._basic_bidg.total_area)            
        return self._area
        
    @property
    def land_area(self):
        if not self._land_area:        
            if self._basic_stead:
                self._land_area = number2xml(self._basic_stead.total_area_sotka or '')
        return self._land_area
    
    @property
    def floor(self):
        if not self._floor:
            if self._basic_bidg:
                self._floor = number2xml(self._basic_bidg.floor)
        return self._floor
    
    @property
    def floors(self):
        if not self._floors:
            if self._basic_bidg:
                floor_count = self._basic_bidg.floor_count
                if floor_count is not None:
                    self._floors = number2xml(int(floor_count))
        return self._floors
        
    def images(self, max_images, clear_watermark=True):        
        from urlparse import urljoin       
        from sorl.thumbnail import get_thumbnail              
        images = self._estate.images.all()[:max_images]
        if images:
            result = []
            for img in images:
                try:               
                    im = get_thumbnail(img.image.file, '800x600', clear_watermark=clear_watermark)
                    head, tail = os.path.split(im.name)  # @UnusedVariable                                
                    result.append(urljoin(self._domain, im.url))                  
                except:
                    logger.debug('Wrong image file %s, lot %s!' % (img.image.file, img.estate))                    
            return result       

class AvitoMapper(BaseMapper):    
    _id = None
    _category = None
    _title = None
    _house_type = None
    _walls_type = None
    _market_type = None
    _object_type = None 
    
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
    
    @property
    def title(self):
        if not self._title:
            self._title = self._estate.estate_category.name
        return self._title

    @property
    def house_type(self):
        if not self._house_type:
            if self._basic_bidg:                
                self._house_type = BaseMapper.get_value_mapper(WallConstrucion, self._basic_bidg.wall_construcion_id, 'HouseType')
        return self._house_type            
    
    @property
    def walls_type(self):
        if not self._house_type:
            if self._basic_bidg:                
                self._house_type = BaseMapper.get_value_mapper(WallConstrucion, self._basic_bidg.wall_construcion_id, 'WallsType')
        return self._house_type
         
    @property
    def market_type(self):
        if not self._market_type:
            self._market_type = u'Вторичка'
        return self._market_type
        
    @property
    def object_type(self):
        if not self._object_type:
            estate_type_id = None
            if self._estate.estate_category.is_stead and self._basic_stead:
                estate_type_id = self._basic_stead.estate_type_id
            elif self._basic_bidg:
                estate_type_id = self._basic_bidg.estate_type_id                         
            if estate_type_id:                
                self._object_type = BaseMapper.get_value_mapper(EstateType, estate_type_id, 'ObjectType')
        return self._object_type
      
    @property
    def operation_type(self):        
        return u'Продам'
    
    @property
    def ad_status(self):
        return u'Free'
        
    @property
    def allow_email(self):
        return u'Да'
