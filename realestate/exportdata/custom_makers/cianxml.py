# -*- coding: utf-8 -*-
from estatebase.models import EstateTypeCategory, Layout, Estate
from exportdata.custom_makers.yaxml import COMMERCE_STEADS, YandexWrapper
from exportdata.custom_makers.yaxmlplus import YandexPlusXML
from exportdata.utils import EstateTypeMapper, LayoutTypeMapper
from exportdata.xml_makers import SalesAgent, number2xml
from lxml import etree
import random

class CianWrapper(YandexWrapper):
    def estate_type(self):        
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE:
            return u'коммерческая'
        if self._basic_stead and self._basic_stead.estate_type_id in COMMERCE_STEADS:
            return u'коммерческая'
        return u'жилая'
    
    def estate_category(self):
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE and self._basic_bidg:             
            return self.estate_type_com_mapper(self._basic_bidg.estate_type_id) 
        return super(CianWrapper, self).estate_category()
    
    def living_space(self):
        used_area = self._basic_bidg.used_area
        if used_area:
            return number2xml(used_area)        
        return number2xml(round(random.uniform(0.55, 0.62) * round(self._basic_bidg.total_area), 1))
            
    def kuhnya_area(self):
        KUHNYA_AREA_DEFAULT = round(random.uniform(9, 12), 1)        
        kuhnya_area = self._basic_bidg.get_kuhnya_area()
        result = kuhnya_area if kuhnya_area else KUHNYA_AREA_DEFAULT
        return number2xml(result)
    
    def estate_type_com_mapper(self, estate_type_id):
        DEFAULT = u'свободного назначения'
        mapper = {
                  EstateTypeMapper.SKLAD : u'склад',
                  EstateTypeMapper.KAFE : u'общепит',
                  EstateTypeMapper.RESTORAN : u'общепит',
                  EstateTypeMapper.TORGOVYYPAVILON : u'торговое помещение',
                  EstateTypeMapper.MAGAZIN : u'торговое помещение',
                  EstateTypeMapper.GOSTINICHNYYKOMPLEKS : u'готовый бизнес',
                  EstateTypeMapper.PROIZVODSTVENNOSKLADSKAYABAZA : u'готовый бизнес',
                  EstateTypeMapper.KONNOSPORTIVNYYKOMPLEKS : u'готовый бизнес',
                  EstateTypeMapper.PROMYSHLENNAYABAZA : u'готовый бизнес',
                  }    
        if estate_type_id in mapper:
            return mapper[estate_type_id]
        return DEFAULT

class CianFlatsXML(YandexPlusXML):
    name = 'cianflats'    
    root_name = 'flats_for_sale'    
    def __init__(self, cian_wrapper):
        super(CianFlatsXML,self).__init__(cian_wrapper)
        self.NSMAP = None
        self.XHTML = ''
            
    def get_root_name(self):
        return self.root_name
            
    def add_header(self, xhtml):
        pass
    
    def get_queryset(self):
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),             
             'agency_price__gte': MIN_PRICE_LIMIT,
             'estate_category_id': EstateTypeCategory.KVARTIRA             
             }
        q = Estate.objects.all()
        q = q.filter(**f)        
        q = q.exclude(street__name__exact = u'без улицы')        
        return q    
            
    def create_offer(self, estate):
        self._wrapper.set_estate(estate)        
        #sa = SalesAgent(estate)
        offer = etree.Element("offer")        
        etree.SubElement(offer, "id").text = str(estate.id)        
        etree.SubElement(offer, "rooms_num").text = self._wrapper.rooms()         
        area = {'total': self._wrapper.area(), 'kitchen': self._wrapper.kuhnya_area(), 'living': self._wrapper.living_space()}
        etree.SubElement(offer, "area", area)
        etree.SubElement(offer, "price", currency=self._wrapper.price.currency()).text = self._wrapper.price.value()       
        return offer

class CianCommerceXML(CianFlatsXML):
    name = 'ciancommerce'    
    root_name = 'commerce'
    