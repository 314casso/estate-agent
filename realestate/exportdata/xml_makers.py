# -*- coding: utf-8 -*-
from lxml import etree
import pytz
import datetime
import sys
import re
from estatebase.models import Estate, Locality, EstateTypeCategory, EstateType
import os
from django.contrib.sites.models import Site
from django.template import loader
from django.template.context import Context
from django.template.defaultfilters import striptags
from django.core.cache import cache
import cPickle as pickle
from settings import MEDIA_ROOT

def memoize(function):
    memo = {}
    def wrapper(*args):
        if args in memo:            
            return memo[args]
        else:             
            memo[args] = function(*args)
            return memo[args]
    return wrapper

def number2xml(d):
    return '%.12g' % d if d else ''

class EstateBaseWrapper(object):
    def __init__(self, estate):
        self._estate = estate
        self._price = self.Price(estate)
        self._domain = 'http://%s' % Site.objects.get_current().domain
        self._basic_bidg = self._estate.basic_bidg 
        self._basic_stead = self._estate.basic_stead
        
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
    
    @memoize
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
    
    @memoize
    def sub_locality(self):
        #Район города
        microdistrict = self._estate.microdistrict
        if microdistrict is not None:          
            return u'%s' % self._estate.microdistrict
                
    def address(self):
        return u'%s' % self._estate.street
    
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
        @memoize
        def period(self):            
            return None   
        
        #единица площади (рекомендуемые значения — «кв. м», «гектар», «cотка», «sq.m», «hectare»)
        @memoize
        def unit(self):
            return None
    
    def images(self):        
        from urlparse import urljoin       
        from sorl.thumbnail import get_thumbnail              
        images = self._estate.images.all()[:4]
        if images:
            result = []
            for img in images:
                try:               
                    im = get_thumbnail(img.image.file, '800x600')
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
    
    @memoize
    def living_space(self):
        # жилая площадь (при продаже комнаты — площадь комнаты)
        if self._basic_bidg:
            return number2xml(self._basic_bidg.used_area)
    
    def lot_area(self):        
        if self._basic_stead:
            return number2xml(self._basic_stead.total_area_sotka or '')
    
    def lot_type(self):
        return self._estate.estate_type
    
    @memoize
    def new_flat(self):
        NEW_FLAT = 34
        if self._basic_bidg:
            return self._basic_bidg.estate_type_id == NEW_FLAT
    
    @memoize    
    def rooms(self):
        if self._basic_bidg:
            return number2xml(self._basic_bidg.room_count)

    @memoize
    def rooms_offered(self):
        return
    
    @memoize
    def phone(self):
        CONNECTED = 3        
        if self._estate.telephony_id == CONNECTED:
            return True 
                    
    @memoize
    def internet(self):
        CONNECTED = 3        
        if self._estate.internet_id == CONNECTED:
            return True
   
    @memoize
    def floor(self):
        if self._basic_bidg:
            return number2xml(self._basic_bidg.floor)
    
    @memoize
    def floors_total(self):
        if self._basic_bidg:
            floor_count = self._basic_bidg.floor_count
            if floor_count is not None:
                return number2xml(int(floor_count))
   
    @memoize
    def building_type(self):
        # матириал стен
        if self._basic_bidg:
            return self._basic_bidg.wall_construcion.name
    
    @memoize
    def built_year(self):        
        if self._basic_bidg:
            return number2xml(self._basic_bidg.year_built)
   
    @memoize
    def lift(self):
        if self._basic_bidg and self._basic_bidg.elevator:
            return True

    @memoize
    def ceiling_height(self):        
        if self._basic_bidg:
            return number2xml(self._basic_bidg.ceiling_height)
    
    @memoize
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
   
    @memoize
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
    
    @memoize
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
    
    @memoize
    def electricity_supply(self):
        PODKLUCHENO = 5
        NO = 7
        true_ids = (PODKLUCHENO,)
        fk = self._estate.electricity_id
        if fk in true_ids:
            return True
        if fk == NO:
            return False
    
    @memoize
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
    
    @memoize
    def agency_id(self):        
        return None
    
    def url(self):        
        return 'http://www.domnatamani.ru/'
    
    def email(self):        
        return 'pochta@domanayuge.ru'

class YandexWrapper(EstateBaseWrapper):  
    category_mapper =  {EstateTypeCategory.KVARTIRAU4ASTOK:u'коттедж',}
    type_mapper = {EstateType.KOMNATA:u'комната'}
    def lot_type(self):
#         mapper = {u'Участок для строительства дома':u'ИЖЗ'}
#         if self._estate.estate_type in mapper:             
#             return mapper[self._estate.estate_type]
        return self._estate.estate_type    
    
    @memoize
    def estate_category(self):       
        cat_id = self._estate.estate_category_id
        if cat_id == EstateTypeCategory.KVARTIRA and self._basic_bidg is not None:
            type_id = self._basic_bidg.estate_type_id
            if type_id in self.type_mapper:
                return self.type_mapper[type_id]            
        if cat_id in self.category_mapper:
            return self.category_mapper[cat_id]
        result = u'%s' % self._estate.estate_category
        return result.lower()
    
    @memoize
    def address(self):        
        if self._estate.locality.locality_type_id == Locality.CITY:
            if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:
                return u'%s, %s' % (super(YandexWrapper, self).address(), self._estate.estate_number) 
            return super(YandexWrapper, self).address()        

class BaseXML(object):
    CACHE_TIME = 3600 * 24  
    VALID_DAYS = 45
    def get_delta(self):    
        return datetime.datetime.now() - datetime.timedelta(days=self.VALID_DAYS)
    def get_cache_key(self, estate):
        return '%s%s' % (self.name, estate.id) 
        
    def get_cache(self, estate):        
        pickled_cache = cache.get(self.get_cache_key(estate))
        if pickled_cache:
            cached_dict = pickle.loads(pickled_cache)
            if cached_dict['modificated'] == estate.history.modificated:
                offer = etree.XML(cached_dict['str_xml'])
                return offer
    
    def set_cache(self, estate, offer):
        str_xml = etree.tostring(offer)
        pickled_dict = {'str_xml':str_xml, 'modificated':estate.history.modificated}
        pickle_xml = pickle.dumps(pickled_dict)
        cache.set(self.get_cache_key(estate), pickle_xml, self.CACHE_TIME)

class YandexXML(BaseXML):
    name = 'yaxml'   
    def __init__(self, use_cache=True):                
        self.XHTML_NAMESPACE = "http://webmaster.yandex.ru/schemas/feed/realty/2010-06"
        self.XHTML = "{%s}" % self.XHTML_NAMESPACE
        self.NSMAP = {None : self.XHTML_NAMESPACE}
        self.tz = pytz.timezone('Europe/Moscow')
        #self.file_name = sys.stdout
        self.file_name = os.path.join(MEDIA_ROOT, 'feed' ,'%s.xml' % self.name)
        self._use_cache = use_cache
        
    def feed_date(self, date):        
        return self.tz.localize(date).replace(microsecond=0).isoformat()
        
    def get_root_name(self):
        return "realty-feed"    
    
    def generation_date(self):        
        return self.feed_date(datetime.datetime.now())
    
    def unit_wrapper(self, etree, parent, value, unit=u'кв.м', value_elem='value', unit_elem='unit'):
        if value:
            etree.SubElement(parent, value_elem).text = value
            etree.SubElement(parent, unit_elem).text = unit    
    
    def bool_to_value(self, bool_value):
        return u'да' if bool_value else u'нет'
    
    def add_bool_element(self, etree, parent, name, value):
        if not value is None:             
            etree.SubElement(parent, name).text = self.bool_to_value(value)
    
    def create_offer(self, estate):
        is_stead = estate.estate_category.is_stead
        has_stead = estate.estate_category.can_has_stead and estate.basic_stead
        estate_wrapper = YandexWrapper(estate)
        sa = SalesAgent(estate)
        #offer
        offer = etree.Element("offer", {'internal-id':str(estate.id)})     
        etree.SubElement(offer, "type").text = estate_wrapper.offer_type()         
        etree.SubElement(offer, "property-type").text = estate_wrapper.estate_type()
        etree.SubElement(offer, "category").text = estate_wrapper.estate_category()
        etree.SubElement(offer, "url").text = estate_wrapper.url()        
        etree.SubElement(offer, "creation-date").text = self.feed_date(estate_wrapper.creation_date())
        if estate_wrapper.last_update_date():
            etree.SubElement(offer, "last-update-date").text = self.feed_date(estate_wrapper.last_update_date())
        #location    
        location = etree.SubElement(offer, "location")
        etree.SubElement(location, "country").text = estate_wrapper.country()
        etree.SubElement(location, "region").text = estate_wrapper.region()
        etree.SubElement(location, "district").text = estate_wrapper.district()
        etree.SubElement(location, "locality-name").text = estate_wrapper.locality()
        if estate_wrapper.sub_locality():
            etree.SubElement(location, "sub-locality-name").text = estate_wrapper.sub_locality()
        if estate_wrapper.address():
            etree.SubElement(location, "address").text = estate_wrapper.address()
        #sales-agent
        sales_agent = etree.SubElement(offer, "sales-agent")
        for phone in sa.phones():
            etree.SubElement(sales_agent, "phone").text = phone  
        etree.SubElement(sales_agent, "category").text = sa.category()
        etree.SubElement(sales_agent, "organization").text = sa.organization()
        if sa.agency_id():
            etree.SubElement(sales_agent, "agency-id").text = sa.agency_id()        
        etree.SubElement(sales_agent, "url").text = sa.url()
        etree.SubElement(sales_agent, "email").text = sa.email()
        #price
        price = etree.SubElement(offer, "price")
        etree.SubElement(price, "value").text = estate_wrapper.price.value()
        etree.SubElement(price, "currency").text = estate_wrapper.price.currency()
        if estate_wrapper.price.period():
            etree.SubElement(price, "period").text = estate_wrapper.price.period()
        if estate_wrapper.price.unit():
            etree.SubElement(price, "unit").text = estate_wrapper.price.unit()
        images = estate_wrapper.images()
        if images:
            for image in images:
                etree.SubElement(offer, "image").text = image            
        etree.SubElement(offer, "description").text = estate_wrapper.description()
        if not is_stead:
            self.unit_wrapper(etree, etree.SubElement(offer, "area"), estate_wrapper.area())
            if estate_wrapper.living_space():
                self.unit_wrapper(etree, etree.SubElement(offer, "living-space"), estate_wrapper.living_space())
        else:
            etree.SubElement(offer, "lot-type").text = estate_wrapper.lot_type()            
        if has_stead: 
            self.unit_wrapper(etree, etree.SubElement(offer, "lot-area"), estate_wrapper.lot_area(), u'сот')
        self.add_bool_element(etree, offer, 'new-flat', estate_wrapper.new_flat())     
        if estate_wrapper.rooms():
            etree.SubElement(offer, "rooms").text = estate_wrapper.rooms()        
        if estate_wrapper.rooms_offered():
            etree.SubElement(offer, "rooms-offered").text = estate_wrapper.rooms_offered()        
        self.add_bool_element(etree, offer, 'phone', estate_wrapper.phone())        
        self.add_bool_element(etree, offer, 'internet', estate_wrapper.internet())
        if estate_wrapper.floor():
            etree.SubElement(offer, "floor").text = estate_wrapper.floor()        
        if estate_wrapper.floors_total():
            etree.SubElement(offer, "floors-total").text = estate_wrapper.floors_total()        
        if estate_wrapper.building_type():
            etree.SubElement(offer, "building-type").text = estate_wrapper.building_type()        
        if estate_wrapper.built_year():
            etree.SubElement(offer, "built-year").text = estate_wrapper.built_year()        
        self.add_bool_element(etree, offer, 'lift', estate_wrapper.lift())                
        if estate_wrapper.ceiling_height():
            etree.SubElement(offer, "ceiling-height").text = estate_wrapper.ceiling_height()        
        self.add_bool_element(etree, offer, 'heating-supply', estate_wrapper.heating_supply())
        self.add_bool_element(etree, offer, 'water-supply', estate_wrapper.water_supply())
        self.add_bool_element(etree, offer, 'sewerage-supply', estate_wrapper.sewerage_supply())
        self.add_bool_element(etree, offer, 'electricity-supply', estate_wrapper.electricity_supply())
        self.add_bool_element(etree, offer, 'gas-supply', estate_wrapper.gas_supply())        
        return offer
    
    def get_offer(self, estate):
        if not estate.is_web_published:
            return 
        if self._use_cache: 
            offer = self.get_cache(estate)
            if offer is not None:
                return offer            
        offer = self.create_offer(estate)        
        self.set_cache(estate, offer)   
        return offer    
    
    def get_filter(self):         
        MIN_PRICE_LIMIT = 100000   
        allowed_categories = (EstateTypeCategory.DOM,EstateTypeCategory.U4ASTOK,EstateTypeCategory.KVARTIRA,EstateTypeCategory.KVARTIRAU4ASTOK)        
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),
             'estate_category__in': allowed_categories,
             'agency_price__gte': MIN_PRICE_LIMIT,             
             }
        return f
    
    def exclude(self, q):
        disallowed_steads = (20,42,51)
        q = q.exclude(street__name__exact = u'без улицы')
        q = q.exclude(stead__estate_type_id__in = disallowed_steads)
        return q
    
    def gen_XML(self):        
        xhtml = etree.Element(self.XHTML + self.get_root_name(), nsmap=self.NSMAP) 
        etree.SubElement(xhtml, "generation-date").text = self.generation_date()                   
        print datetime.datetime.now()
        c = 0    
        q = Estate.objects.filter(**self.get_filter())
        q = self.exclude(q)        
        print  u"%s" % q.query
        for estate in q:
            offer = self.get_offer(estate)
            if offer is not None:                                  
                xhtml.append(self.get_offer(estate))
                c+=1    
        etree.ElementTree(xhtml).write(self.file_name, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        print datetime.datetime.now()
        print c
         


