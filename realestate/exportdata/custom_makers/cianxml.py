# -*- coding: utf-8 -*-
from estatebase.models import EstateTypeCategory, Layout, Estate, EstateType
from exportdata.custom_makers.yaxml import COMMERCE_STEADS, YandexWrapper
from exportdata.custom_makers.yaxmlplus import YandexPlusXML
from exportdata.utils import EstateTypeMapper, LayoutTypeMapper,\
    WallConstrucionMapper
from exportdata.xml_makers import SalesAgent, number2xml
from lxml import etree
import random
import re

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
        
    def new_flat(self):
        new_flat = super(CianWrapper,self).new_flat()        
        return '2' if new_flat else '1'
    
    def sale_type(self):
        return 'F'
    
    def phone(self):
        phone = super(CianWrapper,self).phone()        
        return 'yes' if phone else 'no'
    
    def lift_p(self):
        lift = super(CianWrapper,self).lift()        
        return '1' if lift else '0'
        
    def lift_g(self):
        if super(CianWrapper,self).new_flat():
            return self.lift_p()
        return '0'
    
    def balcon(self):
#         TODO:
        return '0'
    
    def lodgia(self):
        #         TODO:
        return '0'
    
    def su_s(self):
        '''
        количество совмещенных санузлов
        '''
        #         TODO:
        return '0'
    
    def su_r(self):
        '''
        количество раздельных санузлов
        '''
        #         TODO:
        return '0'
        
    def windows(self):
        '''
        куда выходят окна
        '''
        #         TODO:
        DVOR = '1'
        ULITSTA = '2'
        DVOR_ULITSTA = '3'        
        return DVOR_ULITSTA
    
    def ipoteka(self):
        '''
        возможность ипотеки
        '''
        YES = '1'
        NO = '0'
        #         TODO:
        return YES
    
    def floor_type(self):
        '''
        1 – панельный
        2 – кирпичный
        3 – монолитный
        4 – кирпично-монолитный
        5 – блочный
        6 – деревянный
        7 – сталинский
        '''
        mapper = { 
                  WallConstrucionMapper.PANEL: '1', WallConstrucionMapper.KIRPICH: '2', WallConstrucionMapper.MONOLIT: '3', WallConstrucionMapper.BLOK: '5',
                  WallConstrucionMapper.DEREVO: '6'
                 }        
        wall_construcion_id = self._basic_bidg.wall_construcion_id
        if wall_construcion_id in mapper:
            return mapper.get(wall_construcion_id)
        if super(CianWrapper,self).new_flat():
            return '3'
        return '1'
    
    def locality(self):
        GOROD = 1
        pref = []
        if self._estate.locality.locality_type_id != GOROD:             
            pref.append(self._estate.locality.region.regular_name)
            locality_type = self._estate.locality.locality_type.name.lower()
            pref.append(locality_type)
        if pref:
            pref_str = u', '.join(pref)
            return u'%s %s' % (pref_str, self._estate.locality.name)   
        return self._estate.locality.name
    
    def street(self):
        return u'%s %s' % (self._estate.street.street_type or '', self._estate.street.name)
             
    
class CianFlatsXML(YandexPlusXML):
    encoding="windows-1251"
    name = 'cianflats'    
    root_name = 'flats_for_sale'        
    def __init__(self, cian_wrapper):
        super(CianFlatsXML,self).__init__(cian_wrapper)
        self.NSMAP = None
        self.XHTML = ''
            
    def get_root_name(self):
        return self.root_name
    
    def get_queryset(self):        
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),             
             'agency_price__gte': MIN_PRICE_LIMIT,
             'estate_category_id': EstateTypeCategory.KVARTIRA,
             'street__isnull': False,             
             }
        q = Estate.objects.all()
        q = q.filter(**f)
        return q    
            
    def create_offer(self, estate):                
        self._wrapper.set_estate(estate)
        sa = SalesAgent(estate)
        offer = etree.Element("offer")        
        etree.SubElement(offer, "id").text = str(estate.id)        
        etree.SubElement(offer, "rooms_num").text = self._wrapper.rooms()         
        area = {'total': self._wrapper.area(), 'kitchen': self._wrapper.kuhnya_area(), 'living': self._wrapper.living_space()}
        etree.SubElement(offer, "area", area)
        etree.SubElement(offer, "price", currency=self._wrapper.price.currency()).text = self._wrapper.price.value()        
        options = {
                   'object_type':  self._wrapper.new_flat(), 'sale_type':  self._wrapper.sale_type(),
                   'phone':  self._wrapper.phone(), 'lift_p':  self._wrapper.lift_p(), 'lift_g':  self._wrapper.lift_g(),
                   'balcon':  self._wrapper.balcon(), 'lodgia':  self._wrapper.lodgia(), 'su_s':  self._wrapper.su_s(), 
                   'su_r':  self._wrapper.su_r(), 'windows':  self._wrapper.windows(), 'ipoteka':  self._wrapper.ipoteka(),
                   }
        etree.SubElement(offer, "options", options)
        floor = {'total': self._wrapper.floors_total(), 'type': self._wrapper.floor_type()}      
        etree.SubElement(offer, "floor", floor).text = self._wrapper.floors_total()
        etree.SubElement(offer, "note").text = etree.CDATA(self._wrapper.description())
        etree.SubElement(offer, "phone").text = ';'.join([re.sub(r'\D','',phone) for phone in sa.phones()])
        address = {'admin_area': '72', 'locality': self._wrapper.locality(), 'street': self._wrapper.street()}
        etree.SubElement(offer, "address", address)
        images = self._wrapper.images()
        if images:
            for image in images:
                etree.SubElement(offer, "photo").text = image
        return offer

class CianCommerceXML(CianFlatsXML):
    name = 'ciancommerce'    
    root_name = 'commerce'
    