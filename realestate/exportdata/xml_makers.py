# -*- coding: utf-8 -*-
from lxml import etree
import pytz
from datetime import datetime
import sys
import re
from estatebase.models import Estate, Locality
import os
from django.contrib.sites.models import Site
from django.template import loader
from django.template.context import Context

def memoize(function):
    memo = {}
    def wrapper(*args):
        if args in memo:            
            return memo[args]
        else:             
            memo[args] = function(*args)
            return memo[args]
    return wrapper

class EstateBaseWrapper(object):
    def __init__(self, estate):
        self._estate = estate
        self._price = self.Price(estate)
        self._domain = 'http://%s' % Site.objects.get_current().domain
                
        
    def offer_type(self):
        return u'продажа'
    
    def estate_type(self):
        return u'жилая'
    
    def estate_category(self):
        #«комната», «квартира», «дом», «участок», «таунхаус», «часть дома», «дом с участком», «дача», «земельный участок»
        #квартир, комнат, домов и участков
        return u'квартира'
    
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
    
    def sub_locality(self):
        #Район города
        return self._estate.microdistrict.name
                
    def address(self):
        return self._estate.street.name
    
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
        return self.render_content(self._estate, description)  
    
    def area(self):
        # общая площадь
        return "1000"
    
    def living_space(self):
        # жилая площадь (при продаже комнаты — площадь комнаты)
        return "1000"
    
    def lot_area(self):
        # жилая площадь (при продаже комнаты — площадь комнаты)
        return "1000"
    
    def lot_type(self):
        return u"ИЖС"
    
    @memoize
    def new_flat(self):
        return True
    
    @memoize    
    def rooms(self):
        return str(5)

    @memoize
    def rooms_offered(self):
        return str(2)
    
    @memoize
    def phone(self):
        return True
            
    @memoize
    def internet(self):
        return True
   
    @memoize
    def floor(self):
        return str(5)
    
    @memoize
    def floors_total(self):
        return str(5)
   
    @memoize
    def building_type(self):
        # матириал стен
        return u'бетон'
    
    @memoize
    def built_year(self):
        # матириал стен
        return str(2014)
   
    @memoize
    def lift(self):
        return True

    @memoize
    def ceiling_height(self):
        return str(2.95)        
    
    @memoize
    def heating_supply(self):
        return True
   
    @memoize
    def water_supply(self):
        return True
    
    @memoize
    def sewerage_supply(self):
        return True
    
    @memoize
    def electricity_supply(self):
        return True
    
    @memoize
    def gas_supply(self):
        return True
        
class SalesAgent(object):
    def __init__(self, estate):
        self._estate = estate
    def phones(self):
        return ['+7 918...', '8 862...']
    
    def category(self):
        return u'агентство'    
    
    def organization(self):
        return u'Название организации'
    
    @memoize
    def agency_id(self):        
        return None
    
    def url(self):        
        return 'http://domna...'
    
    def email(self):        
        return 'mail@...'

class YandexXML(object):    
    def __init__(self):                
        self.XHTML_NAMESPACE = "http://webmaster.yandex.ru/schemas/feed/realty/2010-06"
        self.XHTML = "{%s}" % self.XHTML_NAMESPACE
        self.NSMAP = {None : self.XHTML_NAMESPACE}
        self.tz = pytz.timezone('Europe/Moscow')
        self.file_name = sys.stdout
        
    def feed_date(self, date):        
        return self.tz.localize(date).replace(microsecond=0).isoformat()
        
    def get_root_name(self):
        return "realty-feed"    
    
    def generation_date(self):        
        return self.feed_date(datetime.now())
    
    def unit_wrapper(self, etree, parent, value, unit=u'кв.м', value_elem='value', unit_elem='unit'):
        if value:
            etree.SubElement(parent, value_elem).text = value
            etree.SubElement(parent, unit_elem).text = unit    
    
    def bool_to_value(self, bool_value):
        return u'да' if bool_value else u'нет'
    
    def add_bool_element(self, etree, parent, name, value):
        if not value is None:             
            etree.SubElement(parent, name).text = self.bool_to_value(value)
        
    
    def add_offer(self, xhtml, estate):        
        is_stead = True #False #estate.estate_category.is_stead
        has_stead = True
        estate_wrapper = EstateBaseWrapper(estate)
        sa = SalesAgent(estate)
        #offer
        offer = etree.SubElement(xhtml, "offer", {'internal-id':str(estate.id)})     
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
        etree.SubElement(location, "sub-locality-name").text = estate_wrapper.sub_locality()
        if True:
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
        for image in estate_wrapper.images():
            etree.SubElement(offer, "image").text = image            
        etree.SubElement(offer, "description").text = estate_wrapper.description()
        if not is_stead:
            self.unit_wrapper(etree, etree.SubElement(offer, "area"), estate_wrapper.area())
            self.unit_wrapper(etree, etree.SubElement(offer, "living-space"), estate_wrapper.living_space())
        else:
            etree.SubElement(offer, "lot-type").text = estate_wrapper.lot_type()            
        if has_stead: 
            self.unit_wrapper(etree, etree.SubElement(offer, "lot-area"), estate_wrapper.lot_area())
       
       
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
    
    def gen_XML(self):        
        xhtml = etree.Element(self.XHTML + self.get_root_name(), nsmap=self.NSMAP) 
        etree.SubElement(xhtml, "generation-date").text = self.generation_date()
        estate = Estate.objects.get(pk=103600)                
        self.add_offer(xhtml, estate)    
        etree.ElementTree(xhtml).write(self.file_name, pretty_print=True, xml_declaration=True, encoding="UTF-8") 


