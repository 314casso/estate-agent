# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
from realty.fields_parser import BaseFieldsParser
from realty.utils import join_strings
from realty.items import RealtyItem
from estatebase.models import EstateType, Locality
from scrapy.selector import Selector
import re

class OrbitaTamanFleldsParser(BaseFieldsParser):
    _razdel = None
    def title_parser(self):
        return self.sel.xpath('b/text()').extract()
                  
    def razdel_from_url(self):
        if self._razdel:
            return self._razdel
        if self.url:
            from urlparse import urlparse, parse_qs        
            query = parse_qs(urlparse(self.url).query)
            if 'razdel' in query:
                self._razdel = query['razdel'][0]
                return self._razdel
        return None
                         
    def estate_type_parser(self):        
        razdel_map = {
                      '08117': u'коммерческая',
                      }
        mapper = {
                         ur'гараж' : 9,
                         ur'комн\.' : 6,
                         ur'квартир' : 6,
                         ur'комнат' : 21,
                         ur'дома|коттеджа' : 39,
                         ur'дом\b|домо|хату' : 16,                         
                         ur'часть' : 18,
                         ur'дачу' : 13,
                         ur'домик' : 13,
                         ur'коттедж\b' : 22,
                         ur'участ': 15,
                         ur'пай': 15,
                         ur'коммерческая': self.commerce_parser,                        
                         }
        txt = razdel_map[self.razdel_from_url()] if self.razdel_from_url() in razdel_map else self.title()
        txt = re.sub('\d|\s|\/','', txt)        
        result = None                
        parts = txt.split()        
        if parts:           
            result = self.re_mapper(mapper, parts[0])
            if callable(result):
                return result()
        return result or self.ZDANIE
    
    def commerce_parser(self):
        COMMERCE_CAT_ID = 6       
        txt = self.title()        
        key = 'commerce_mapper_smart'  
        from django.core.cache import cache
        mapper = cache.get(key)
        if not mapper:                                
            types = EstateType.objects.filter(estate_type_category_id=COMMERCE_CAT_ID) 
            mapper = {}
            for t in types:
                mapper[ur'%s' % t.name] = t.id
                mapper[ur'%s' % t.name_accs] = t.id
            cache.set(key, mapper, 3600)         
        return self.re_mapper(mapper, txt) or self.ZDANIE 
    
    def phone_parser(self):    
        return self.sel.re(ur'\d\-\d[\d|\-]+')
    
    def room_count_parser(self):
        matches = re.search(ur'(\d)\-КОМН', self.title(), re.U | re.I)
        if matches:
            return matches.group(0)
        
    def link(self):
        import hashlib
        id_instead_link = hashlib.md5(join_strings(self.sel.xpath('text()').extract()).encode('utf-8')).hexdigest()
        return [id_instead_link]
        
    def region_parser(self):
        if self.locality_id:
            return Locality.objects.get(pk=self.locality_id).region_id
        return self.TEMRUK
    
    def locality_parser(self):         
        return join_strings(self.sel.re(ur'(?:п\.|ст\.|x\.|г\.)\s(\D+?)\,')) or u'Темрюк'
    
    def name_parser(self):
        return [u'неизвестно']
    
    def desc_parser(self):
        result = []
        result.append(self.title().lower().capitalize())        
        result.append(join_strings(self.sel.xpath('text()').extract(), ', '))                
        return [join_strings(result, ' ')]
    
    def price_parser(self):        
        return self.sel.re(ur'(\d[\d|\s]+)\sруб.')
    
    def mesure_parser(self):
        return u'руб.'
    
    def locality_id(self):
        TEMRUK_ID = 110 
        if not self._locality_id:
            self._locality_id = self.get_locality() 
            if not self._locality_id:
                self._locality_id = self.get_locality(field_name='name_loct')                
        return self._locality_id or TEMRUK_ID
    
    def phone(self):
        PHONECODE = '86148'
        phones = self.filter_phone()
        if phones:
            return ['8%s%s' % (PHONECODE, phone) if 5 <= len(phone) < 10 else phone for phone in phones]
        
    def get_locality(self, field_name='name'):
        txt = self.locality_parser() 
        if not txt:
            return None        
        key = 'localities_mapper_%s' % field_name        
        from django.core.cache import cache
        mapper = cache.get(key)        
        if not mapper:                                
            localities = Locality.objects.all()
            mapper = {}            
            for locality in localities:
                mapper[ur'%s' % getattr(locality, field_name)] = locality.id
            cache.set(key, mapper, 3600)  
        return self.re_mapper(mapper, txt)

class OrbitaTamanSpider(CrawlSpider):   
    ORIGIN_ID = 11 
    name = 'orbitataman'
    allowed_domains = ['orbitataman.ru']
    start_urls = [     
                  'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=08110&maxi=100',                  
                  'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=08111&maxi=100',
                  'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=08112&maxi=100',
                  'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=08113&maxi=100',
                  'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=08114&maxi=100',
                  'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=08115&maxi=100',
                  'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=08116&maxi=100',
                  'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=08117&maxi=100',
                  'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=09110&maxi=100',
                  'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=09111&maxi=100',
                  'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=14110&maxi=100',
                  ]
         
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="niz"]',)), callback='parse_item'),
    )  
    
    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url, level=log.INFO)
        sel = Selector(response)
        entries = sel.xpath("//td[@width='88%']/div[@class='text12']")
        for entry in entries:       
            fields_parser = OrbitaTamanFleldsParser(entry, response.url)
            item = RealtyItem()
            print fields_parser.phone()
            fields_parser.populate_item(item)                        
            yield item     
