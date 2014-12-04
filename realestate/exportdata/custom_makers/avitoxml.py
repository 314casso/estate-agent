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
from exportdata.models import FeedLocality

class AvitoWrapper(YandexWrapper):
    category_mapper =  {
                        EstateTypeCategory.KVARTIRAU4ASTOK:u'Дома, дачи, коттеджи', EstateTypeCategory.KVARTIRA:u'Квартиры',
                        EstateTypeCategory.DOM:u'Дома, дачи, коттеджи', EstateTypeCategory.U4ASTOK: u'Земельные участки',
                        }
    type_mapper = {EstateTypeMapper.KOMNATA:u'Комнаты'}
    def estate_type(self):        
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE:
            return u'коммерческая'
        if self._basic_stead and self._basic_stead.estate_type_id in COMMERCE_STEADS:
            return u'коммерческая'
        return u'жилая'
    
    def distance_to_city(self):
        if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:
            return
        return u'0'
        
    def sale_rooms(self):
        if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:
            self.rooms()
        
    
    def object_type(self):
        if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:
            return
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE:
            return self.estate_type_com_mapper(self._basic_bidg.estate_type_id)
        if self._estate.estate_category_id in (EstateTypeCategory.DOM, EstateTypeCategory.KVARTIRAU4ASTOK):             
            type_mapper = {
                           EstateTypeMapper.DACHA:u'Дача',
                           EstateTypeMapper.DOM:u'Дом',
                           EstateTypeMapper.POLDOMA:u'Таунхаус',
                           EstateTypeMapper.KVARTIRASUCHASTKOM:u'Таунхаус',
                           EstateTypeMapper.KOTTEDZH:u'Коттедж',
                           EstateTypeMapper.TAUNHAUS:u'Таунхаус',
                           EstateTypeMapper.DUPLEKS:u'Таунхаус',                       
                           }
            return type_mapper.get(self._basic_bidg.estate_type_id) 
        if self._estate.estate_category_id == EstateTypeCategory.U4ASTOK:
            type_mapper = {
                           EstateTypeMapper.DACHNYYUCHASTOK :u'Сельхозназначения (СНТ, ДНП)',
                           EstateTypeMapper.UCHASTOKDLYASTROITELSTVADOMA:u'Поселений (ИЖС)',
                           EstateTypeMapper.UCHASTOKSELSKOHOZYAYSTVENNOGONAZNACHENIYA:u'Сельхозназначения (СНТ, ДНП)',
                           EstateTypeMapper.UCHASTOKKOMMERCHESKOGONAZNACHENIYA:u'Промназначения',
                           EstateTypeMapper.UCHASTOKINOGONAZNACHENIYA:u'Промназначения',                                                  
                           }
            return type_mapper.get(self._basic_stead.estate_type_id)
            
    def feed_locality(self, feed_name):
        result = {}
        try:
            feed_locality = FeedLocality.objects.get(feed_name=feed_name, locality=self._estate.locality)
            result['city'] = feed_locality.locality.name
            return result            
        except FeedLocality.DoesNotExist:
            result['city'] = self._estate.locality.region.metropolis.name
            result['locality'] = self._estate.locality.name
            return result
    
    def ad_status(self):
        return u'Free'             
     
    def offer_type(self):
        return u'Продам'
    
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
        new_flat = super(AvitoWrapper,self).new_flat()        
        return u'Новостройка' if new_flat else u'Вторичка'
    
    def sale_type(self):
        return 'F'
    
    def phone(self):
        phone = super(AvitoWrapper,self).phone()        
        return 'yes' if phone else 'no'
    
    def lift_p(self):
        if super(AvitoWrapper,self).new_flat():
            return '1'
        lift = super(AvitoWrapper,self).lift()        
        return '1' if lift else '0'
        
    def lift_g(self):
        if super(AvitoWrapper,self).new_flat():
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
    
    def house_type(self):
        if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:    
            mapper = { 
                      WallConstrucionMapper.PANEL: u'Панельный', WallConstrucionMapper.KIRPICH: u'Кирпичный', 
                      WallConstrucionMapper.MONOLIT: u'Монолитный', WallConstrucionMapper.BLOK: u'Блочный',
                      WallConstrucionMapper.DEREVO: u'Деревянный'
                     }        
            wall_construcion_id = self._basic_bidg.wall_construcion_id
            if wall_construcion_id in mapper:
                return mapper.get(wall_construcion_id)        
            
    def walls_type(self):
        if not self._estate.estate_category_id == EstateTypeCategory.KVARTIRA and self._basic_bidg:    
            mapper = { 
                      WallConstrucionMapper.PANEL: u'Ж/б панели', WallConstrucionMapper.KIRPICH: u'Кирпич', 
                      WallConstrucionMapper.PENOBLOK: u'Пеноблоки', WallConstrucionMapper.PENOBETON:u'Пеноблоки', 
                      WallConstrucionMapper.DEREVO: u'Бревно', WallConstrucionMapper.BRUS:u'Брус', 
                      WallConstrucionMapper.METALL:u'Металл', WallConstrucionMapper.BLOK:u'Пеноблоки', 
                     }        
            wall_construcion_id = self._basic_bidg.wall_construcion_id
            if wall_construcion_id in mapper:
                return mapper.get(wall_construcion_id)
    
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
             
    
class AvitoXML(YandexPlusXML):    
    name = 'avito'    
    root_name = 'Ads'           
    def __init__(self, avito_wrapper):
        super(AvitoXML,self).__init__(avito_wrapper)        
        self.NSMAP = None
        self.XHTML = ''
            
    def get_root_name(self):
        return self.root_name
    
    def get_XHTML(self, use_cache):
        xhtml = super(AvitoXML,self).get_XHTML(use_cache)        
        xhtml.set("target", "Avito.ru")
        xhtml.set("formatVersion", "2")                
        return xhtml
    
    def get_queryset(self):        
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),             
             'agency_price__gte': MIN_PRICE_LIMIT,
             'estate_category_id__in': (EstateTypeCategory.KVARTIRA, EstateTypeCategory.DOM, EstateTypeCategory.KVARTIRAU4ASTOK, EstateTypeCategory.U4ASTOK),
             'street__isnull': False,
             'estate_params__exact': EstateParam.PAYEXPORT,             
             }
        q = Estate.objects.all()
        q = q.filter(**f)
        return q    
            
    def create_offer(self, estate):                
        self._wrapper.set_estate(estate)
        sa = SalesAgent(estate)
        offer = etree.Element("Ad")
        etree.SubElement(offer, "Id").text = str(estate.id)
        category = self._wrapper.estate_category() 
        etree.SubElement(offer, "Category").text = category
        etree.SubElement(offer, "OperationType").text = self._wrapper.offer_type()
        if self._wrapper.sale_rooms():
            etree.SubElement(offer, "SaleRooms").text = self._wrapper.sale_rooms()
        if self._wrapper.rooms():
            etree.SubElement(offer, "Rooms").text = self._wrapper.rooms()
        if category == u'Комнаты':             
            if self._wrapper.living_space():
                etree.SubElement(offer, "Square").text = self._wrapper.living_space()
        else:
            if self._wrapper.area():
                etree.SubElement(offer, "Square").text = self._wrapper.area()
        
        if self._wrapper.lot_area():
            etree.SubElement(offer, "LandArea").text = self._wrapper.lot_area()
            
        if self._wrapper.distance_to_city() is not None:
            etree.SubElement(offer, "DistanceToCity").text = self._wrapper.distance_to_city()
                
        if self._wrapper.floor():            
            etree.SubElement(offer, "Floor").text = self._wrapper.floor()        
        if self._wrapper.floors_total():
            etree.SubElement(offer, "Floors").text = self._wrapper.floors_total()
        
        if self._wrapper.house_type():
            etree.SubElement(offer, "HouseType").text = self._wrapper.house_type()
        
        if self._wrapper.walls_type():
            etree.SubElement(offer, "WallsType").text = self._wrapper.walls_type()

        if estate.estate_category_id == EstateTypeCategory.KVARTIRA:
            etree.SubElement(offer, "MarketType").text = self._wrapper.new_flat()
        
        
                
        etree.SubElement(offer, "Region").text = self._wrapper.region()
        feed_locality = self._wrapper.feed_locality(self.name)
        etree.SubElement(offer, "City").text = feed_locality['city']
        if 'locality' in feed_locality:
            etree.SubElement(offer, "Locality").text = feed_locality['locality']
        
        etree.SubElement(offer, "District").text = self._wrapper.district()                            
        etree.SubElement(offer, "Street").text = self._wrapper.street()
        
        etree.SubElement(offer, "ObjectType").text = self._wrapper.object_type()
        
        
        etree.SubElement(offer, "Description").text = self._wrapper.description()
        etree.SubElement(offer, "Price").text = self._wrapper.price.value()
        images = self._wrapper.images(True)
        if images:
            images_root = etree.SubElement(offer, "Images")        
            if images:
                for image in images:
                    image_node = etree.SubElement(images_root, "Image")
                    image_node.set("url", image)
        etree.SubElement(offer, "CompanyName").text = sa.organization()
        etree.SubElement(offer, "EMail").text = sa.email()
        etree.SubElement(offer, "ContactPhone").text = sa.phones()[0]
        etree.SubElement(offer, "AdStatus").text = self._wrapper.ad_status()
        return offer   