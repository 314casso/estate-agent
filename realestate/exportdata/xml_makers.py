# -*- coding: utf-8 -*-
from lxml import etree
import datetime
import re
import os
from django.contrib.sites.models import Site
from django.template import loader
from django.template.context import Context
from django.template.defaultfilters import striptags
from django.core.cache import cache
import cPickle as pickle
from estatebase.models import Locality
import pytz
from settings import MEDIA_ROOT
from exportdata.utils import EstateTypeMapper
from django.utils import translation

def number2xml(d):
    return '%.12g' % d if d else ''

class EstateBaseWrapper(object):
    _layout = None
    def __init__(self):        
        self._domain = 'http://%s' % Site.objects.get_current().domain
    
    def set_estate(self, estate):
        self._estate = estate
        self._price = self.Price(estate)        
        self._basic_bidg = self._estate.basic_bidg 
        self._basic_stead = self._estate.basic_stead
        self._layout = None
        
    def offer_type(self):
        return u'продажа'
    
    def estate_type(self):
        return u'жилая'
    
    def estate_category(self):
        #«комната», «квартира», «дом», «участок», «таунхаус», «часть дома», «дом с участком», «дача», «земельный участок»
        #квартир, комнат, домов и участков
        result = u'%s' % self._estate.estate_category
        return result.lower()
    
    def url(self):        
        return 'http://www.domnatamani.ru/?p=%s' % self._estate.wp_meta.post_id              
    
    def creation_date(self):
        return self._estate.history.created
    
    def last_update_date(self):        
        return self._estate.history.updated

    def country(self):
        return u'Россия'
    
    def region(self):
        return u'Краснодарский край'
    
    def district(self):
        return self._estate.region.regular_name
    
    def locality(self):
        return self._estate.locality.name
    
    def sub_locality(self):
        #Район города
        microdistrict = self._estate.microdistrict
        if microdistrict is not None:          
            return u'%s' % self._estate.microdistrict
                
    def address(self):
        if self._estate.street:
            return u'%s %s' % (self._estate.street.name, self._estate.street.street_type or '')
        return ''
    
    @property
    def price(self):
        return self._price
    
    class Price(object):
        def __init__(self, estate):
            self._estate = estate     
        def value(self):
            return re.sub(r'\s', '', str(self._estate.agency_price)) 
        
        def currency(self):
            return "RUB"
        
        #в случае сдачи недвижимости в аренду — промежуток времени (рекомендуемые значения — «день», «месяц», «day», «month»)
        def period(self):            
            return None   
        
        #единица площади (рекомендуемые значения — «кв. м», «гектар», «cотка», «sq.m», «hectare»)
        def unit(self):
            return None
    
    def images(self, clear_watermark=False):        
        from urlparse import urljoin       
        from sorl.thumbnail import get_thumbnail              
        images = self._estate.images.all()[:4]
        if images:
            result = []
            for img in images:
                try:               
                    im = get_thumbnail(img.image.file, '800x600', clear_watermark=clear_watermark)
                    head, tail = os.path.split(im.name)  # @UnusedVariable                                
                    result.append(urljoin(self._domain, im.url))                  
                except IOError:
                    pass                    
            return result
    
    def render_content(self, estate, description):        
        t = loader.get_template('reports/feed/text_content.html')
        c = Context({'estate_item':estate, 'description': description})
        rendered = t.render(c)
        return re.sub(r"\s+"," ", rendered).strip()
    
    def render_post_description(self, estate):
        region = u'Краснодарского края' if estate.locality.locality_type_id == Locality.CITY else estate.locality.region.regular_name_gent
        location = u'%s %s' % (estate.locality.name_loct, region)
        result = u'Продается %s в %s' % (estate.estate_type.lower(), location)             
        return result
    
    def description(self):
        description = self.render_post_description(self._estate)
        return striptags(self.render_content(self._estate, description))  
    
    def area(self):
        # общая площадь
        if self._basic_bidg:
            return number2xml(self._basic_bidg.total_area)
    
    def living_space(self):
        # жилая площадь (при продаже комнаты — площадь комнаты)
        if self._basic_bidg:
            return number2xml(self._basic_bidg.used_area)
    
    def lot_area(self):        
        if self._basic_stead:
            return number2xml(self._basic_stead.total_area_sotka or '')
    
    def lot_type(self):
        return self._estate.estate_type
    
    
    def new_flat(self):        
        if self._basic_bidg:
            return self._basic_bidg.estate_type_id == EstateTypeMapper.NOVOSTROYKA 
        
    def rooms(self):
        if self._basic_bidg:
            return number2xml(self._basic_bidg.room_count)

    def rooms_offered(self):
        return
    
    def phone(self):
        CONNECTED = 3        
        if self._estate.telephony_id == CONNECTED:
            return True 
                    
    def internet(self):
        CONNECTED = 3        
        if self._estate.internet_id == CONNECTED:
            return True
   
    def floor(self):
        if self._basic_bidg:
            return number2xml(self._basic_bidg.floor)
    
    
    def floors_total(self):
        if self._basic_bidg:
            floor_count = self._basic_bidg.floor_count
            if floor_count is not None:
                return number2xml(int(floor_count))
   
    def building_type(self):
        # матириал стен
        if self._basic_bidg:
            return self._basic_bidg.wall_construcion.name
    
    def built_year(self):        
        if self._basic_bidg:
            return number2xml(self._basic_bidg.year_built)
   
    def lift(self):
        if self._basic_bidg and self._basic_bidg.elevator:
            return True
    
    def ceiling_height(self):        
        if self._basic_bidg:
            return number2xml(self._basic_bidg.ceiling_height)
    
    def heating_supply(self):
        PERSONAL_GAS = 1
        PERSONAL_TD = 2
        PERSONAL_ELECTRIC = 3
        CENTRAL = 4
        NO = 8
        true_ids = (PERSONAL_GAS,PERSONAL_TD,PERSONAL_ELECTRIC,CENTRAL)        
        if self._basic_bidg:
            fk = self._basic_bidg.heating_id
            if fk in true_ids:
                return True
            if fk == NO:
                return False 
   
    def water_supply(self):
        VODOPROVOD = 1
        PODKLUCHENO = 7  
        NO = 10      
        true_ids = (VODOPROVOD,PODKLUCHENO)
        fk = self._estate.watersupply_id        
        if fk in true_ids:
            return True
        if fk == NO:
            return False
    
    def sewerage_supply(self):
        PODKLUCHENO = 5
        CENTRAL = 8
        NO = 9
        true_ids = (CENTRAL,PODKLUCHENO)
        fk = self._estate.sewerage_id
        if fk in true_ids:
            return True
        if fk == NO:
            return False
    
    def electricity_supply(self):
        PODKLUCHENO = 5
        NO = 7
        true_ids = (PODKLUCHENO,)
        fk = self._estate.electricity_id
        if fk in true_ids:
            return True
        if fk == NO:
            return False
    
    def gas_supply(self):
        PODKLUCHENO = 5
        NO = 7
        true_ids = (PODKLUCHENO,)
        fk = self._estate.gassupply_id
        if fk in true_ids:
            return True
        if fk == NO:
            return False
        
class SalesAgent(object):
    def __init__(self, estate):
        self._estate = estate
    def phones(self):      
        return ['8-800-250-7075', '8-918-049-9494']
    
    def category(self):
        return u'агентство'    
    
    def organization(self):
        return u'Дома на юге'
    
    
    def agency_id(self):        
        return None
    
    def url(self):        
        return 'http://www.domnatamani.ru/'
    
    def email(self):        
        return 'pochta@domanayuge.ru'

class BaseXML(object):
    CACHE_TIME = 3600 * 24  
    VALID_DAYS = 44
    XHTML_NAMESPACE = None
    def __init__(self):               
        self.XHTML = "{%s}" % self.XHTML_NAMESPACE
        self.NSMAP = {None : self.XHTML_NAMESPACE}
        self.tz = pytz.timezone('Europe/Moscow')        
        self.file_name = os.path.join(MEDIA_ROOT, 'feed' ,'%s.xml' % self.name)        
        self._use_cache = True
        translation.activate('ru')
    def get_delta(self):    
        return datetime.datetime.now() - datetime.timedelta(days=self.VALID_DAYS)
    def get_cache_key(self, estate):
        return '%s%s' % (self.name, estate.id) 
        
    def get_cache(self, estate):        
        pickled_cache = cache.get(self.get_cache_key(estate))
        if pickled_cache:
            cached_dict = pickle.loads(pickled_cache)
            if cached_dict['modificated'] == estate.history.modificated:
                parser = etree.XMLParser(strip_cdata=False)
                offer = etree.XML(cached_dict['str_xml'], parser)                
                return offer
    
    def set_cache(self, estate, offer):
        str_xml = etree.tostring(offer, encoding='unicode')         
        pickled_dict = {'str_xml':str_xml, 'modificated':estate.history.modificated}
        pickle_xml = pickle.dumps(pickled_dict)
        cache.set(self.get_cache_key(estate), pickle_xml, self.CACHE_TIME)




