# -*- coding: utf-8 -*-
from estatebase.models import Estate, EstateTypeCategory, EstateParam, Locality,\
    YES
from exportdata.xml_makers import SalesAgent, number2xml
from lxml import etree
from exportdata.custom_makers.yaxml import YandexWrapper
from exportdata.custom_makers.yaxmlplus import YandexPlusXML
from exportdata.utils import EstateTypeMapper, WallConstrucionMapper
from django.template.defaultfilters import striptags


class NndvWrapper(YandexWrapper):  
    def offer_type(self):
        return u'продам'
    
    def address(self):        
        if self.is_outoftown():
            return None         
        if self._estate.street:
            return u'%s %s' % (self._estate.street.name, self._estate.street.street_type or '')
        return ''
    
    def description(self):
        description = self.render_post_description(self._estate)
        return striptags(self.render_content(self._estate, description, True))
    
    def kuhnya_area(self):
        if self._basic_bidg:         
            kuhnya_area = self._basic_bidg.get_kuhnya_area()
            result = kuhnya_area if kuhnya_area else None
        return number2xml(result)    
    
    def get_item_name(self):
        if self.is_flat():
            estate_type_id = self._basic_bidg.estate_type_id
            mapper = {
                        EstateTypeMapper.NOVOSTROYKA: u'building',
                        EstateTypeMapper.KOMNATA: u'room',
                     }
            if estate_type_id in mapper:
                return mapper[estate_type_id] 
            return u'flat' 
        if self.is_commerce():
            return u'commerce'        
        if self.is_outoftown():
            return u'outoftown'                
        return u'other'    
    
    def get_object_type(self):                
        if self.is_flat():
            return                
        if self.is_commerce():
            return self.get_commerce_object()
        if self.is_outoftown():         
            return self.get_outoftown_object()   
        return self.get_other_object()
    
    def is_flat(self):
        if self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:
            if self._basic_bidg:
                return True
        return False
        
    def is_commerce(self):
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE:        
            return True
        if self._estate.estate_category_id == EstateTypeCategory.U4ASTOK and self._estate.com_status == YES:
            return True            
        return False
    
    def is_outoftown(self):         
        if self._estate.locality.locality_type != Locality.CITY and not self.is_flat() and not self.is_commerce():
            return True
        return False
    
    def update_mapper_uchastok(self, type_mapper, common_name):        
        uchastok_mapper = {
                       EstateTypeMapper.DACHNYYUCHASTOK :common_name,
                       EstateTypeMapper.UCHASTOKDLYASTROITELSTVADOMA:common_name,
                       EstateTypeMapper.UCHASTOKSELSKOHOZYAYSTVENNOGONAZNACHENIYA:common_name,
                       EstateTypeMapper.UCHASTOKKOMMERCHESKOGONAZNACHENIYA:common_name,
                       EstateTypeMapper.UCHASTOKINOGONAZNACHENIYA:common_name,                                                  
                       }
        type_mapper.update(uchastok_mapper)
        return type_mapper
        
    def get_commerce_object(self):
        type_mapper = {                  
                       EstateTypeMapper.ZDANIEGARAZHNYHBOKSOV :u'гараж',
                       EstateTypeMapper.ZDANIE :u'здание',                                             
                       EstateTypeMapper.ADMINISTRATIVNOTORGOVOEZDANIE :u'торговый павильон',                                                                             
                       EstateTypeMapper.TORGOVYYPAVILON :u'торговый павильон',
                       EstateTypeMapper.MAGAZIN :u'магазин',                       
                       EstateTypeMapper.OFIS :u'офис',
                       EstateTypeMapper.ADMINISTRATIVNOEZDANIE :u'офис',                      
                       EstateTypeMapper.SKLAD :u'складское',
                       EstateTypeMapper.PROIZVODSTVENNOSKLADSKAYABAZA :u'производств. помещ.',
                       EstateTypeMapper.PROIZVODSTVENNAYABAZA: u'производств. помещ.',
                       }
        type_mapper = self.update_mapper_uchastok(type_mapper, u'земельный участок')
        return self.map_object(type_mapper, u'здание')     
        
    def get_outoftown_object(self):        
        type_mapper = {                  
                       EstateTypeMapper.DACHA:u'дача',
                       EstateTypeMapper.DOM:u'дом',
                       EstateTypeMapper.POLDOMA:u'таунхаус',
                       EstateTypeMapper.KVARTIRASUCHASTKOM:u'таунхаус',
                       EstateTypeMapper.KOTTEDZH:u'коттедж',
                       EstateTypeMapper.TAUNHAUS:u'таунхаус',
                       EstateTypeMapper.DUPLEKS:u'таунхаус',                         
                       }
        type_mapper = self.update_mapper_uchastok(type_mapper, u'участок')
        return self.map_object(type_mapper, u'дом') 
    
    def get_other_object(self):        
        type_mapper = {                  
                       EstateTypeMapper.GARAZH:u'гараж',                       
                       EstateTypeMapper.DOM:u'дом',
                       EstateTypeMapper.POLDOMA:u'полдома',
                       EstateTypeMapper.KVARTIRASUCHASTKOM:u'таунхаус',
                       EstateTypeMapper.KOTTEDZH:u'дом',
                       EstateTypeMapper.TAUNHAUS:u'таунхаус',
                       EstateTypeMapper.DUPLEKS:u'таунхаус',
                       EstateTypeMapper.UCHASTOKDLYASTROITELSTVADOMA:u'участок под ижс',                         
                       }        
        return self.map_object(type_mapper, u'дом') 
    
    def map_object(self, type_mapper, default):       
        estate_type_id = None
        if self._basic_bidg:
            estate_type_id = self._basic_bidg.estate_type_id
        elif self._basic_stead:
            estate_type_id = self._basic_stead.estate_type_id        
        return type_mapper.get(estate_type_id, default)
    
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
             }
        q = Estate.objects.all()
        q = q.filter(**f)        
        q = q.exclude(street__name__exact = u'без улицы')   
        q = q.exclude(estate_params__exact = EstateParam.RENT,)     
        return q
    
    def bool_to_value(self, bool_value):
        return u'есть' if bool_value else u'нет'
    
    def to_int(self, d):
        result = int(float(d))
        return u'%s' % result 
    
    def validate_offer(self, offer):
        flat = ['id', 'region', 'naspunkt', 'oborot', 'money', 'rooms', 'area_sum', 'floors', 'floor', 'address', 'contact_who', 'contact_phone']
        other = ['id', 'region', 'naspunkt', 'oborot', 'money', 'area', 'object', 'address', 'contact_who', 'contact_phone']
        outoftown = ['id', 'region', 'naspunkt', 'oborot', 'money', 'object', 'contact_who', 'contact_phone']
        required = {
                    'building':flat,
                    'room':flat,
                    'flat':flat,
                    'commerce':other,
                    'outoftown':outoftown,
                    'other':other,
                    }
        if offer is None:            
            return False
        item_name = offer.xpath("/*")[0].tag
        required_tags = required.get(item_name)
        for tag in required_tags:
            if not offer.xpath("/*/%s" % tag):
                print 'Validation error! Empty tag %s' % tag
                return False
        comment_len = len(offer.xpath("/*/comment")[0].text)
        if comment_len > 800:
            print 'Validation error! Comment is over %s' % comment_len
            return False            
        return True
    
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
        #price
        etree.SubElement(offer, "money").text = self._wrapper.price.value()   
        images = self._wrapper.images()        
        if images:
            for i,image in enumerate(images, start=1):
                etree.SubElement(offer, "image%s" % i).text = image                    
        etree.SubElement(offer, "comment").text = self._wrapper.description()
        if self._wrapper.is_flat():
            if self._wrapper.rooms():
                etree.SubElement(offer, "rooms").text = self._wrapper.rooms()      
            self.add_bool_element(etree, offer, 'phone', self._wrapper.phone())       
            if self._wrapper.floor():
                etree.SubElement(offer, "floor").text = self._wrapper.floor()        
            if self._wrapper.floors_total():
                etree.SubElement(offer, "floors").text = self._wrapper.floors_total()        
            if self._wrapper.house_type():
                etree.SubElement(offer, "house").text = self._wrapper.house_type()       
            self.add_bool_element(etree, offer, 'lift', self._wrapper.lift())            
            if self._wrapper.area():
                etree.SubElement(offer, "area_sum").text = self.to_int(self._wrapper.area())
            if self._wrapper.living_space():
                etree.SubElement(offer, "area_life").text = self.to_int(self._wrapper.living_space())          
            if self._wrapper.kuhnya_area():
                etree.SubElement(offer, "area_kitchen").text = self.to_int(self._wrapper.kuhnya_area())
        else:
            etree.SubElement(offer, "object").text = self._wrapper.get_object_type()            
            if has_stead and item_name == u'outoftown': 
                etree.SubElement(offer, "area_land").text = self.to_int(self._wrapper.lot_area())
            else:
                etree.SubElement(offer, "area").text = self.to_int(self._wrapper.lot_area()) if is_stead else self.to_int(self._wrapper.area())                       
        return offer 