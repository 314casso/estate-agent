# -*- coding: utf-8 -*-
from estatebase.models import Estate, EstateTypeCategory, EstateParam
from exportdata.xml_makers import SalesAgent, number2xml
from lxml import etree
from exportdata.custom_makers.yaxml import YandexWrapper
from exportdata.custom_makers.yaxmlplus import YandexPlusXML
from exportdata.utils import EstateTypeMapper, WallConstrucionMapper


class NndvWrapper(YandexWrapper):
    category_mapper =  {
                        EstateTypeCategory.KVARTIRAU4ASTOK:u'Дома, дачи, коттеджи', EstateTypeCategory.KVARTIRA:u'flat',
                        EstateTypeCategory.DOM:u'Дома, дачи, коттеджи', EstateTypeCategory.U4ASTOK: u'Земельные участки',
                        EstateTypeCategory.COMMERCE: u'Коммерческая недвижимость',
                        }
    
    def offer_type(self):
        return u'продам'
    
    def kuhnya_area(self):
        if self._basic_bidg:         
            kuhnya_area = self._basic_bidg.get_kuhnya_area()
            result = kuhnya_area if kuhnya_area else None
        return number2xml(result)    
    
    def get_item_name(self):
        if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:
            if self._basic_bidg:
                estate_type_id = self._basic_bidg.estate_type_id
                mapper = {
                            EstateTypeMapper.NOVOSTROYKA: u'building',
                            EstateTypeMapper.KOMNATA: u'room',
                         }
                if estate_type_id in mapper:
                    return mapper[estate_type_id] 
                return u'flat'  
        if self._estate.estate_category_id in (EstateTypeCategory.DOM, EstateTypeCategory.KVARTIRAU4ASTOK, EstateTypeCategory.U4ASTOK):
            return u'outoftown'
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE:
            return u'commerce'
        return u'other'    
    
    def get_object_type(self):
        if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:
            return        
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
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE:
            DEFAULT = u'здание';
            estate_type_id = None
            if self._basic_bidg:
                estate_type_id = self._basic_bidg.estate_type_id
            elif self._basic_stead:
                estate_type_id = self._basic_stead.estate_type_id
            type_mapper = {                  
                           EstateTypeMapper.ADMINISTRATIVNOTORGOVOEZDANIE :u'Торговое помещение',                                                                            
                           EstateTypeMapper.TORGOVYYPAVILON :u'Торговое помещение',
                           EstateTypeMapper.MAGAZIN :u'Торговое помещение',
                           EstateTypeMapper.GOSTINITSA :u'Гостиница',
                           EstateTypeMapper.GOSTEVOYDOM :u'Гостиница',
                           EstateTypeMapper.GOSTEVYEKOMNATY :u'Гостиница',
                           EstateTypeMapper.GOSTINICHNYYKOMPLEKS :u'Гостиница',
                           EstateTypeMapper.PANSIONAT :u'Гостиница',
                           EstateTypeMapper.OTEL :u'Гостиница',
                           EstateTypeMapper.MINIGOSTINITSA :u'Гостиница',
                           EstateTypeMapper.SANATORIY :u'Гостиница',
                           EstateTypeMapper.OFIS :u'Офисное помещение',
                           EstateTypeMapper.ADMINISTRATIVNOEZDANIE :u'Офисное помещение',
                           EstateTypeMapper.RESTORAN :u'Ресторан, кафе',
                           EstateTypeMapper.KAFE :u'Ресторан, кафе',
                           EstateTypeMapper.SALONKRASOTY :u'Салон красоты',
                           EstateTypeMapper.SKLAD :u'Складское помещение',
                           EstateTypeMapper.PROIZVODSTVENNOSKLADSKAYABAZA :u'Складское помещение',                           
                           }
            return type_mapper.get(estate_type_id, DEFAULT) 
    
    def is_flat(self, item_name):
        flat_items = (u'flat', u'room', u'building')
        if item_name in flat_items:
            return True 
    
    def house_type(self): 
        if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:    
            mapper = { 
                      WallConstrucionMapper.PANEL: u'панельный', WallConstrucionMapper.KIRPICH: u'кирпичный',  
                      WallConstrucionMapper.MONOLIT: u'монолит', WallConstrucionMapper.BLOK: u'блочный',
                      WallConstrucionMapper.DEREVO: u'дерев.'
                     }        
            wall_construcion_id = self._basic_bidg.wall_construcion_id
            if wall_construcion_id in mapper:
                return mapper.get(wall_construcion_id)            


class NndvXML(YandexPlusXML):
    name = 'nndvxml'
    XHTML_NAMESPACE = "http://nndv.ru/xml"
    def __init__(self, nndv_wrapper):
        super(NndvXML,self).__init__(nndv_wrapper)
        
    def get_root_name(self):
        return "items"
    
    def get_root_params(self):
        return {'version':'1'}
    
    def get_XHTML(self, use_cache):
        self.set_use_cache(use_cache)     
        xhtml = etree.Element(self.XHTML + self.get_root_name(), self.get_root_params(), nsmap=self.NSMAP) 
        self.add_header(xhtml)        
        self.add_offers(xhtml)
        return xhtml
        
    def get_queryset(self):
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),             
             'agency_price__gte': MIN_PRICE_LIMIT, 
             'estate_category_id': EstateTypeCategory.KVARTIRA,            
             }
        q = Estate.objects.all()
        q = q.filter(**f)        
        q = q.exclude(street__name__exact = u'без улицы')   
        q = q.exclude(estate_params__exact = EstateParam.RENT,)     
        return q
    
    def create_offer(self, estate):                
        self._wrapper.set_estate(estate)
        is_stead = estate.estate_category.is_stead
        has_stead = estate.estate_category.can_has_stead and estate.basic_stead        
        sa = SalesAgent(estate)
        #offer
        item_name = self._wrapper.get_item_name()
        
        offer = etree.Element(item_name)
        etree.SubElement(offer, "id").text = str(estate.id)              
        etree.SubElement(offer, "oborot").text = self._wrapper.offer_type()    
        etree.SubElement(offer, "url").text = self._wrapper.url()        
        etree.SubElement(offer, "creation-date").text = self.feed_date(self._wrapper.creation_date())
        if self._wrapper.last_update_date():
            etree.SubElement(offer, "last-update-date").text = self.feed_date(self._wrapper.last_update_date())
        #location  
        etree.SubElement(offer, "country").text = self._wrapper.country()
        etree.SubElement(offer, "region").text = self._wrapper.region()
        etree.SubElement(offer, "rayon").text = self._wrapper.district()
        etree.SubElement(offer, "naspunkt").text = self._wrapper.locality()        
        if self._wrapper.address():
            etree.SubElement(offer, "address").text = self._wrapper.address()
        #sales-agent
        sales_agent = offer        
        etree.SubElement(sales_agent, "contact_phone").text = sa.phones()[0]  
        etree.SubElement(sales_agent, "contact_who").text = sa.category()
        etree.SubElement(sales_agent, "contact_firma").text = sa.organization()
        etree.SubElement(sales_agent, "contact_email").text = sa.email()        
        if sa.agency_id():
            etree.SubElement(sales_agent, "agency-id").text = sa.agency_id()        
        etree.SubElement(sales_agent, "url").text = sa.url()
        etree.SubElement(sales_agent, "email").text = sa.email()
        #price
        etree.SubElement(offer, "money").text = self._wrapper.price.value()   
        images = self._wrapper.images()
        if images:
            for image in images:
                etree.SubElement(offer, "image").text = image            
        etree.SubElement(offer, "comment").text = self._wrapper.description()
        if self._wrapper.is_flat(item_name):
            if self._wrapper.area():
                etree.SubElement(offer, "area_sum").text = self._wrapper.area()
            if self._wrapper.living_space():
                etree.SubElement(offer, "area_life").text = self._wrapper.living_space()          
            if self._wrapper.kuhnya_area():
                etree.SubElement(offer, "area_kitchen").text = self._wrapper.kuhnya_area()
        else:
            etree.SubElement(offer, "object").text = self._wrapper.get_object_type()            
            if has_stead and item_name == u'outoftown': 
                etree.SubElement(offer, "area_land").text = self._wrapper.lot_area()
            else:
                etree.SubElement(offer, "area").text = self._wrapper.lot_area() if is_stead else self._wrapper.area()
                         
        if self._wrapper.rooms():
            etree.SubElement(offer, "rooms").text = self._wrapper.rooms()      
        self.add_bool_element(etree, offer, 'phone', self._wrapper.phone())        
        self.add_bool_element(etree, offer, 'internet', self._wrapper.internet())
        if self._wrapper.floor():
            etree.SubElement(offer, "floor").text = self._wrapper.floor()        
        if self._wrapper.floors_total():
            etree.SubElement(offer, "floors").text = self._wrapper.floors_total()        
        if self._wrapper.house_type():
            etree.SubElement(offer, "house").text = self._wrapper.house_type()       
        self.add_bool_element(etree, offer, 'lift', self._wrapper.lift())               
        return offer 