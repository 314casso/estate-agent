# -*- coding: utf-8 -*-
from estatebase.models import Estate, EstateTypeCategory, EstateParam
from exportdata.custom_makers.yaxml import YandexWrapper, YandexXML,\
    COMMERCE_STEADS
import os
from lxml import etree

class YandexPlusWrapper(YandexWrapper):
    def estate_type(self):        
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE:
            return u'коммерческая'
        if self._basic_stead and self._basic_stead.estate_type_id in COMMERCE_STEADS:
            return u'коммерческая'
        return u'жилая'
    
    def estate_category(self):
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE and self._basic_bidg:
            result = u'%s' % self._basic_bidg.estate_type
            return result.lower() 
        return super(YandexPlusWrapper, self).estate_category()

class YandexPlusXML(YandexXML):
    VALID_DAYS = 100
    name = 'yaxmlplus'
    def __init__(self, yandex_plus_wrapper):
        super(YandexPlusXML,self).__init__(yandex_plus_wrapper)         
        
    def get_queryset(self):
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),             
             'agency_price__gte': MIN_PRICE_LIMIT,             
             }
        q = Estate.objects.all()
        q = q.filter(**f)        
        q = q.exclude(street__name__exact = u'без улицы')   
        q = q.exclude(estate_params__exact = EstateParam.RENT,)     
        return q
    
    
  
class AnapaWrapper(YandexWrapper):  
    _domain = 'http://%s' % 'copy.domnatamani.ru'  
    def images(self, clear_watermark=False):        
        from urlparse import urljoin     
        images = self._estate.images.all()
        if images:
            result = []
            for img in images:
                try:               
                    result.append(urljoin(self._domain, img.image.url))                  
                except:
                    pass                    
            return result 
    
    def estate_type(self):        
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE:
            return u'коммерческая'
        if self._basic_stead and self._basic_stead.estate_type_id in COMMERCE_STEADS:
            return u'коммерческая'
        return u'жилая'
    
    def estate_category(self):
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE and self._basic_bidg:
            result = u'%s' % self._basic_bidg.estate_type
            return result.lower() 
        return super(AnapaWrapper, self).estate_category()  
    
class AnapaXML(YandexXML):
    VALID_DAYS = 10
    name = 'anapa'
    def __init__(self, anapa_wrapper):
        super(AnapaXML,self).__init__(anapa_wrapper)
        SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
        self.file_name = os.path.join(SITE_ROOT, '%s.xml' % self.name)         
        
    def get_queryset(self):         
        f = {
             'region__id':1,                        
             'history__modificated__gte':self.get_delta(),
             }
        q = Estate.objects.all()
        q = q.filter(**f)     
        return q    
    
    def create_offer(self, estate):        
        self._wrapper.set_estate(estate)
        is_stead = estate.estate_category.is_stead
        has_stead = estate.estate_category.can_has_stead and estate.basic_stead       
        #offer        
        offer = etree.Element("offer", {'internal-id':str(estate.id), 'anapa':'wake'})     
        etree.SubElement(offer, "type").text = self._wrapper.offer_type()         
        etree.SubElement(offer, "property-type").text = self._wrapper.estate_type()
        etree.SubElement(offer, "category").text = self._wrapper.estate_category()
        etree.SubElement(offer, "url").text = self._wrapper.url()        
        etree.SubElement(offer, "creation-date").text = self.feed_date(self._wrapper.creation_date())
        if self._wrapper.last_update_date():
            etree.SubElement(offer, "last-update-date").text = self.feed_date(self._wrapper.last_update_date())
        
        #contact
        sellers = etree.SubElement(offer, "sellers")
        for client in estate.clients.all(): 
            client_name = u"%s" % client.name
            seller = etree.SubElement(sellers, "seller", {'name': client_name.strip()})            
            for contact in client.contacts.all():
                etree.SubElement(seller, "contact", {'contact':contact.contact, 'type': u"%s" % contact.contact_type.name})
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
            if self._wrapper.kitchen_space():
                self.unit_wrapper(etree, etree.SubElement(offer, "kitchen-space"), self._wrapper.kitchen_space())
            for room_space in self._wrapper.rooms_space():
                self.unit_wrapper(etree, etree.SubElement(offer, "room-space"), room_space)
            if self._wrapper.rooms_type():
                etree.SubElement(offer, "rooms-type").text = self._wrapper.rooms_type()            
            self.add_bool_element(etree, offer, 'kitchen-furniture', self._wrapper.kitchen_furniture())
            self.add_bool_element(etree, offer, 'room-furniture', self._wrapper.room_furniture())
            self.add_bool_element(etree, offer, 'television', self._wrapper.television())
            self.add_bool_element(etree, offer, 'washing-machine', self._wrapper.washing_machine())
            self.add_bool_element(etree, offer, 'refrigerator', self._wrapper.refrigerator())
            self.add_bool_element(etree, offer, 'alarm', self._wrapper.alarm())
        else:
            etree.SubElement(offer, "lot-type").text = self._wrapper.lot_type()            
        if has_stead: 
            self.unit_wrapper(etree, etree.SubElement(offer, "lot-area"), self._wrapper.lot_area(), u'сот')
        self.add_bool_element(etree, offer, 'new-flat', self._wrapper.new_flat())     
        if self._wrapper.rooms():
            etree.SubElement(offer, "rooms").text = self._wrapper.rooms()        
        if self._wrapper.rooms_offered():
            etree.SubElement(offer, "rooms-offered").text = self._wrapper.rooms_offered()
        
        if self._wrapper.is_studio():
            self.add_bool_element(etree, offer, 'open-plan', self._wrapper.is_studio())
                        
        self.add_bool_element(etree, offer, 'phone', self._wrapper.phone())        
        self.add_bool_element(etree, offer, 'internet', self._wrapper.internet())
        self.add_bool_element(etree, offer, 'mortgage', self._wrapper.mortgage())
        
        if self._wrapper.renovation():
            etree.SubElement(offer, "renovation").text = self._wrapper.renovation()
                
        if self._wrapper.quality():
            etree.SubElement(offer, "quality").text = self._wrapper.quality()        
                
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