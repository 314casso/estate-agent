# -*- coding: utf-8 -*-
from estatebase.models import Estate, Locality, EstateTypeCategory, EstateType,\
    EstateParam
import datetime
from exportdata.xml_makers import EstateBaseWrapper, BaseXML, SalesAgent
from lxml import etree
from shutil import copyfile
from exportdata.utils import EstateTypeMapper

COMMERCE_STEADS = (EstateTypeMapper.UCHASTOKKOMMERCHESKOGONAZNACHENIYA,EstateTypeMapper.UCHASTOKSELSKOHOZYAYSTVENNOGONAZNACHENIYA,EstateTypeMapper.UCHASTOKINOGONAZNACHENIYA)

class YandexWrapper(EstateBaseWrapper):  
    category_mapper =  {EstateTypeCategory.KVARTIRAU4ASTOK:u'часть дома',}
    type_mapper = {EstateType.KOMNATA:u'комната'}
    def lot_type(self):
        return self._estate.estate_type    
    
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
    
    def address(self):
        if self._estate.locality.locality_type_id == Locality.CITY:
#             if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA and self._estate.estate_number:
#                 return u'%s, %s' % (super(YandexWrapper, self).address(), self._estate.estate_number) 
            return super(YandexWrapper, self).address() 
        
class YandexXML(BaseXML):
    name = 'yaxml'
    encoding="UTF-8"
    XHTML_NAMESPACE = "http://webmaster.yandex.ru/schemas/feed/realty/2010-06"
    def __init__(self, yandex_wrapper):
        super(YandexXML, self).__init__()   
        self._wrapper = yandex_wrapper           
        
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
        self._wrapper.set_estate(estate)
        is_stead = estate.estate_category.is_stead
        has_stead = estate.estate_category.can_has_stead and estate.basic_stead        
        sa = SalesAgent(estate)
        #offer
        offer = etree.Element("offer", {'internal-id':str(estate.id)})     
        etree.SubElement(offer, "type").text = self._wrapper.offer_type()         
        etree.SubElement(offer, "property-type").text = self._wrapper.estate_type()
        etree.SubElement(offer, "category").text = self._wrapper.estate_category()
        etree.SubElement(offer, "url").text = self._wrapper.url()        
        etree.SubElement(offer, "creation-date").text = self.feed_date(self._wrapper.creation_date())
        if self._wrapper.last_update_date():
            etree.SubElement(offer, "last-update-date").text = self.feed_date(self._wrapper.last_update_date())
        #location    
        location = etree.SubElement(offer, "location")
        etree.SubElement(location, "country").text = self._wrapper.country()
        etree.SubElement(location, "region").text = self._wrapper.region()
        etree.SubElement(location, "district").text = self._wrapper.district()
        etree.SubElement(location, "locality-name").text = self._wrapper.locality()
        if self._wrapper.sub_locality():
            etree.SubElement(location, "sub-locality-name").text = self._wrapper.sub_locality()
        if self._wrapper.address():
            etree.SubElement(location, "address").text = self._wrapper.address()
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
        etree.SubElement(price, "value").text = self._wrapper.price.value()
        etree.SubElement(price, "currency").text = self._wrapper.price.currency()
        if self._wrapper.price.period():
            etree.SubElement(price, "period").text = self._wrapper.price.period()
        if self._wrapper.price.unit():
            etree.SubElement(price, "unit").text = self._wrapper.price.unit()
        images = self._wrapper.images()
        if images:
            for image in images:
                etree.SubElement(offer, "image").text = image            
        etree.SubElement(offer, "description").text = self._wrapper.description()
        if not is_stead:
            self.unit_wrapper(etree, etree.SubElement(offer, "area"), self._wrapper.area())
            if self._wrapper.living_space():
                self.unit_wrapper(etree, etree.SubElement(offer, "living-space"), self._wrapper.living_space())
        else:
            etree.SubElement(offer, "lot-type").text = self._wrapper.lot_type()            
        if has_stead: 
            self.unit_wrapper(etree, etree.SubElement(offer, "lot-area"), self._wrapper.lot_area(), u'сот')
        self.add_bool_element(etree, offer, 'new-flat', self._wrapper.new_flat())     
        if self._wrapper.rooms():
            etree.SubElement(offer, "rooms").text = self._wrapper.rooms()        
        if self._wrapper.rooms_offered():
            etree.SubElement(offer, "rooms-offered").text = self._wrapper.rooms_offered()        
        self.add_bool_element(etree, offer, 'phone', self._wrapper.phone())        
        self.add_bool_element(etree, offer, 'internet', self._wrapper.internet())
        if self._wrapper.floor():
            etree.SubElement(offer, "floor").text = self._wrapper.floor()        
        if self._wrapper.floors_total():
            etree.SubElement(offer, "floors-total").text = self._wrapper.floors_total()        
        if self._wrapper.building_type():
            etree.SubElement(offer, "building-type").text = self._wrapper.building_type()        
        if self._wrapper.built_year():
            etree.SubElement(offer, "built-year").text = self._wrapper.built_year()        
        self.add_bool_element(etree, offer, 'lift', self._wrapper.lift())                
        if self._wrapper.ceiling_height():
            etree.SubElement(offer, "ceiling-height").text = self._wrapper.ceiling_height()        
        self.add_bool_element(etree, offer, 'heating-supply', self._wrapper.heating_supply())
        self.add_bool_element(etree, offer, 'water-supply', self._wrapper.water_supply())
        self.add_bool_element(etree, offer, 'sewerage-supply', self._wrapper.sewerage_supply())
        self.add_bool_element(etree, offer, 'electricity-supply', self._wrapper.electricity_supply())
        self.add_bool_element(etree, offer, 'gas-supply', self._wrapper.gas_supply())        
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

    def get_queryset(self):
        MIN_PRICE_LIMIT = 100000  
        allowed_categories = (EstateTypeCategory.DOM,EstateTypeCategory.U4ASTOK,EstateTypeCategory.KVARTIRA,EstateTypeCategory.KVARTIRAU4ASTOK)        
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),
             'estate_category__in': allowed_categories,
             'agency_price__gte': MIN_PRICE_LIMIT,
             'estate_params__exact': EstateParam.POSTONSITE,
             'street__isnull': False,
             }
        q = Estate.objects.all()
        q = q.filter(**f)        
        q = q.exclude(street__name__exact = u'без улицы')
        q = q.exclude(stead__estate_type_id__in = COMMERCE_STEADS)
        q = q.exclude(estate_params__exact = EstateParam.RENT,)        
        return q
    
    def set_use_cache(self, value):
        self._use_cache = value
    
    def add_header(self, xhtml):
        etree.SubElement(xhtml, "generation-date").text = self.generation_date()
    
    def add_offers(self, xhtml):
        q = self.get_queryset()              
        for estate in q:
            offer = self.get_offer(estate)
            if offer is not None:                                  
                xhtml.append(offer)
    
    def get_XHTML(self, use_cache):
        self.set_use_cache(use_cache)     
        xhtml = etree.Element(self.XHTML + self.get_root_name(), nsmap=self.NSMAP) 
        self.add_header(xhtml)        
        self.add_offers(xhtml)
        return xhtml
    
    def gen_XML(self, use_cache=True):   
        xhtml = self.get_XHTML(use_cache)    
        temp_file_name = u'%s~' % self.file_name
        print temp_file_name
        etree.ElementTree(xhtml).write(temp_file_name, pretty_print=True, xml_declaration=True, encoding=self.encoding)
        copyfile(temp_file_name, self.file_name)        
        