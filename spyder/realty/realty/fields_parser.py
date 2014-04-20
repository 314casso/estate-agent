# -*- coding: utf-8 -*-
import re
from estatebase.models import Locality
from realty.utils import join_strings

def abstractmethod(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method ' + repr(method)) 
    default_abstract_method.__name__ = method.__name__     
    return default_abstract_method

class BaseFieldsParser(object):
    _title = None
    _prices = None
    _locality_id = 0
    _region_id = 0
    ZDANIE = 93
    ANAPA = 1
    GELEN = 2
    NOVOROSS = 3
    TEMRUK = 4   
    def __init__(self, sel, url):                     
        self.sel = sel  
        self.url = url 
    
    @abstractmethod
    def title_parser(self): pass     
    
    @abstractmethod
    def estate_type_parser(self): pass
    
    @abstractmethod
    def phone_parser(self): pass        
    
    @abstractmethod
    def room_count_parser(self): pass
        
    @abstractmethod    
    def region_parser(self): pass
    
    @abstractmethod
    def locality_parser(self): pass
    
    @abstractmethod
    def name_parser(self): pass
    
    @abstractmethod
    def desc_parser(self): pass
    
    @abstractmethod
    def price_parser(self): pass
    
    @abstractmethod
    def mesure_parser(self): pass
    
    def phone(self):
        return self.filter_phone()
    
    def name(self):
        return self.name_parser()
    
    def description(self):
        return self.desc_parser()
    
    def prices(self):
        if not self._prices:            
            price = join_strings(self.price_parser())
            mesure = join_strings(self.mesure_parser())             
            price_str = ['%s %s' % (price, mesure) if price else '']
            price_digit = [self.digit_price(price, mesure)]
            self._prices = {'price' : price_str, 'price_digit' : price_digit}
        return self._prices
    
    def link(self):
        return [self.url]
    
    def estate_type_id(self):
        return self.estate_type_parser()  
    
    def region_id(self):
        if not self._region_id:
            self._region_id = self.region_parser() 
        return self._region_id  
    
    def locality_id(self):
        if not self._locality_id:
            self._locality_id = self.get_locality() 
        return self._locality_id
    
    def room_count(self):
        room_parser_result = self.room_count_parser()
        if room_parser_result:
            result = join_strings(room_parser_result)
            return re.sub('\D','', result)
    
    def populate_item(self, item):        
        item['phone'] = self.phone()         
        item['name'] = self.name()
        item['desc'] = self.description()                    
        item['price'] = self.prices()['price']
        item['price_digit'] = self.prices()['price_digit']
        item['link'] = self.link()
        item['estate_type_id'] = self.estate_type_id()                         
        item['region_id'] = self.region_id()   
        item['locality_id'] = self.locality_id()        
        item['room_count'] = self.room_count()    
    
    def title(self):
        if not self._title:
            self._title = join_strings(self.title_parser())
        return self._title
    
    def re_mapper(self, mapper, txt):
        if txt:
            for key, value in mapper.iteritems():
                matches = re.search(key, txt, re.I | re.U)            
                if matches:
                    return value 
    
    def price_mesures(self):
        return {u'т.р.':1000, u'млн.р.':1000000, u'тыс. руб.':1000, u'руб.': 1}
            
    def digit_price(self, price, mesure):
        mesures = self.price_mesures()
        if price:
            if mesure in mesures:
                price_digit = float(re.sub('\D','', price))
                price_digit = int(price_digit * mesures[mesure])                
                return price_digit
        return 0
    
    def filter_phone(self):
        phone = self.phone_parser()
        if not phone:
            return            
        phone_str = join_strings(phone,',')
        phones = re.split(r'[\,|\n]', phone_str)
        result = []
        for phone in phones:         
            phone = phone.strip().replace('+7', '8')
            result.append(re.sub('\D','', phone))
        return result
            
    def get_locality(self, field_name='name'):
        txt = self.locality_parser() 
        if not txt:
            return None        
        key = 'localities_mapper_%s_%s' % (self.region_id(), field_name) 
        from django.core.cache import cache
        mapper = cache.get(key)
        if not mapper:                                
            localities = Locality.objects.filter(region_id=self.region_id)
            mapper = {}
            for locality in localities:
                mapper[ur'%s' % getattr(locality, field_name)] = locality.id
            cache.set(key, mapper, 3600)  
        return self.re_mapper(mapper, txt)