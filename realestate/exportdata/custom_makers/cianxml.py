# -*- coding: utf-8 -*-
from estatebase.models import EstateTypeCategory, Layout, Estate, EstateType,\
    EstateParam
from exportdata.custom_makers.yaxml import COMMERCE_STEADS, YandexWrapper
from exportdata.custom_makers.yaxmlplus import YandexPlusXML
from exportdata.utils import EstateTypeMapper, LayoutTypeMapper,\
    WallConstrucionMapper
from exportdata.xml_makers import SalesAgent, number2xml
from lxml import etree
import random
import re
from random import shuffle, randrange

class CianWrapper(YandexWrapper):
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
        
    def new_flat(self):
        new_flat = super(CianWrapper,self).new_flat()        
        return '2' if new_flat else '1'
    
    def sale_type(self):
        return 'F'
    
    def phone(self):
        phone = super(CianWrapper,self).phone()        
        return 'yes' if phone else 'no'
    
    def lift_p(self):
        if super(CianWrapper,self).new_flat():
            return '1'
        lift = super(CianWrapper,self).lift()        
        return '1' if lift else '0'
        
    def lift_g(self):
        if super(CianWrapper,self).new_flat():
            return '1'
        return '0'
    
    def format_int_result(self, value, if_none='0'):
        return number2xml(value) if value else if_none
    
    def balcon(self):
        return self.format_int_result(self._basic_bidg.get_balcons_count())
    
    def lodgia(self):
        return self.format_int_result(self._basic_bidg.get_loggias_count())
    
    def su_s(self):
        '''
        количество совмещенных санузлов
        '''
        return self.format_int_result(self._basic_bidg.get_sanuzel_sovmest_count())
    
    def su_r(self):
        '''
        количество раздельных санузлов
        '''       
        sanuzel_razdel_count = self._basic_bidg.get_sanuzel_razdel_count()
        if not sanuzel_razdel_count and not self._basic_bidg.get_sanuzel_sovmest_count():
            return '1'             
        return self.format_int_result(sanuzel_razdel_count)
    
    def windows(self):
        '''
        куда выходят окна
        '''
        #         TODO:
        DVOR = '1'
        ULITSTA = '2'
        DVOR_ULITSTA = '3'
        windows_list = (DVOR, ULITSTA, DVOR_ULITSTA)  
        return random.choice(windows_list)
    
    def ipoteka(self):
        '''
        возможность ипотеки
        '''
        ipoteka = len(self._estate.estate_params.filter(pk=EstateParam.IPOTEKA)) > 0
        YES = '1'
        NO = '0'
        return YES if ipoteka else NO
    
    def split_rooms(self):
        if self._basic_bidg:
            rooms = self._basic_bidg.room_count
            total_area = float(self._basic_bidg.total_area)
            rooms_areas = []
            room_area = int(total_area / rooms)
            remain_area = total_area
            for room in range(rooms-1):
                cur_area = room_area + room_area * randrange(25) * 1.0 / 100
                cur_area = round(cur_area,0) 
                rooms_areas.append(number2xml(cur_area))
                remain_area -= cur_area
            rooms_areas.append(number2xml(remain_area))
            shuffle(rooms_areas)
            return '+'.join(rooms_areas)             
    
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
             'estate_params__exact': EstateParam.PAYEXPORT,            
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

class CianWrapperCom(CianWrapper):
    def commerce_type(self):        
        DEFAULT = u'FP'
        estate_type_id = self._basic_bidg.estate_type_id if self._basic_bidg else None 
        mapper = {
#                     O – офис
#                     W – склад
#                     T – торговая площадь
#                     F – под общепит
#                     FP – помещение свободного назначения
#                     G – гараж
#                     AU – автосервис
#                     WP – производственное помещение
#                     B – отдельно стоящее здание
#                     UA – юридический адрес
#                     SB – продажа бизнеса
#                     BU – под бытовые услуги (салон красоты и т.д.)
                  EstateTypeMapper.SKLAD : u'W',
                  EstateTypeMapper.KAFE : u'F',
                  EstateTypeMapper.RESTORAN : u'F',
                  EstateTypeMapper.TORGOVYYPAVILON : u'T',
                  EstateTypeMapper.MAGAZIN : u'T',
                  EstateTypeMapper.OFIS: u'O',
                  EstateTypeMapper.GARAZH : u'G',
                  EstateTypeMapper.STO : u'AU',
                  EstateTypeMapper.PROIZVODSTVENNAYABAZA : u'WP',
                  EstateTypeMapper.PROMYSHLENNAYABAZA : u'WP',
                  EstateTypeMapper.PROIZVODSTVENNOSKLADSKAYABAZA : u'WP',
                  EstateTypeMapper.ZDANIE : u'B',
                  EstateTypeMapper.SALONKRASOTY : u'BU',
                  EstateTypeMapper.OTEL : u'SB',
                  EstateTypeMapper.GOSTINITSA : u'SB',
                  EstateTypeMapper.GOSTEVOYDOM : u'SB',
                  EstateTypeMapper.GOSTEVYEKOMNATY : u'SB',
                  EstateTypeMapper.GOSTINICHNYYKOMPLEKS : u'SB',               
                  }    
        if estate_type_id in mapper:
            return mapper[estate_type_id]
        return DEFAULT
    
    def contract_type(self):
        return '4'

class CianCommerceXML(CianFlatsXML):
    name = 'ciancommerce'    
    root_name = 'commerce'
    def __init__(self, cian_wrapper_com):
        super(CianCommerceXML,self).__init__(cian_wrapper_com)
    def get_queryset(self):        
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),             
             'agency_price__gte': MIN_PRICE_LIMIT,
             'estate_category_id': EstateTypeCategory.COMMERCE,
             'street__isnull': False, 
             'estate_params__exact': EstateParam.PAYEXPORT,            
             }
        q = Estate.objects.all()
        q = q.filter(**f)
        return q[:1] 
    
    def create_offer(self, estate):                
        self._wrapper.set_estate(estate)
        sa = SalesAgent(estate)
        offer = etree.Element("offer")        
        etree.SubElement(offer, "id").text = str(estate.id)
        etree.SubElement(offer, "commerce_type").text = self._wrapper.commerce_type()
        etree.SubElement(offer, "contract_type").text = self._wrapper.contract_type()
        area = {'total': self._wrapper.area(), 'rooms_count': self._wrapper.rooms(), 'rooms': self._wrapper.split_rooms()}
        etree.SubElement(offer, "area", area)
        
        etree.SubElement(offer, "note").text = etree.CDATA(self._wrapper.description())
        etree.SubElement(offer, "phone").text = ';'.join([re.sub(r'\D','',phone) for phone in sa.phones()])
        address = {'admin_area': '72', 'locality': self._wrapper.locality(), 'street': self._wrapper.street()}
        etree.SubElement(offer, "address", address)
        images = self._wrapper.images()
        if images:
            for image in images:
                etree.SubElement(offer, "photo").text = image
        return offer