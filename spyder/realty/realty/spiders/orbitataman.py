# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
from realty.fields_parser import BaseFieldsParser
from realty.utils import join_strings, process_value_base
from realty.items import RealtyItem
from estatebase.models import EstateType
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
                         ur'комн.' : 6,
                         ur'квартиру' : 6,
                         ur'комнат' : 21,
                         ur'дом' : 16,
                         ur'дача' : 13,
                         ur'коттедж' : 16,
                         ur'участок': 15,
                         ur'коммерческая': self.commerce_parser,
                         ur'гостиница': 12,
                         }
        txt = razdel_map[self.razdel_from_url()] if self.razdel_from_url() in razdel_map else self.title() 
        parts = txt.split()
        if parts:           
            result = self.re_mapper(mapper, parts[0])
            if callable(result):
                return result()
        return result or self.ZDANIE
    
    def commerce_parser(self):
        COMMERCE_CAT_ID = 6       
        txt = u'%s ' % self.title()  
        print txt
        key = 'commerce_mapper_smart'  
        from django.core.cache import cache
        mapper = cache.get(key)
        if not mapper:                                
            types = EstateType.objects.filter(estate_type_category_id=COMMERCE_CAT_ID) 
            mapper = {}
            for t in types:
                mapper[ur'%s\s' % t.name] = t.id
                mapper[ur'%s\s' % t.name_accs] = t.id
            cache.set(key, mapper, 3600)         
        return self.re_mapper(mapper, txt) or self.ZDANIE 
    
    def phone_parser(self):    
        return self.sel.re(ur'\d[\d|\-]+\.')
    
    def room_count_parser(self):
        matches = re.search(ur'(\d)\-КОМН', self.title(), re.U | re.I)
        if matches:
            return matches.group(0)
        
    def link(self):
        import hashlib
        id_instead_link = hashlib.md5(join_strings(self.sel.xpath('text()').extract()).encode('utf-8')).hexdigest()
        return [id_instead_link]
        
    def region_parser(self):
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
        if not self._locality_id:
            self._locality_id = self.get_locality() 
        return self._locality_id
    
    def phone(self):
        PHONECODE = '86148'
        phones = self.filter_phone()
        if phones:
            return ['8%s%s' % (PHONECODE, phone) if 5 <= len(phone) < 10 else phone for phone in phones]

def process_value(value):            
    return process_value_base(value, OrbitaTamanSpider.name)

class OrbitaTamanSpider(CrawlSpider):   
    ORIGIN_ID = 8 
    name = 'orbitataman'
    allowed_domains = ['orbitataman.ru']
    start_urls = [                       
#                   'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=08111&maxi=100',
#                   'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=08112&maxi=100',
#                   'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=08116&maxi=100', 
                  'http://orbitataman.ru/modules.php?name=Obyavlen&op=viewob&razdel=08117&maxi=100',   
                  ]
         
    rules = (
        #Rule(SgmlLinkExtractor(restrict_xpaths=('//td[@width="52%" and @height="14" and @valign="middle"]/a[@class="niz"]',)), follow=True),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="niz"]',)), callback='parse_item'),
        #Rule (SgmlLinkExtractor(restrict_xpaths=('//a[@class="more_link"]',), process_value=process_value), callback='parse_item')
    )  
    
    def parse_start_url(self, response):
        yield self.parse_item(response)

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url, level=log.INFO)
        sel = Selector(response)
        entries = sel.xpath("//td[@width='88%']/div[@class='text12']")
        for entry in entries:
#             print '*'*50
#             print join_strings(entry.xpath("b/text()").extract())
#             print join_strings(entry.xpath("text()").extract())
#             print '*'*50        
         
            fields_parser = OrbitaTamanFleldsParser(entry, response.url)
#             print fields_parser.title()
            print join_strings(fields_parser.description())
#             print fields_parser.room_count()
#             print fields_parser.phone()
#             print fields_parser.prices()['price']
#             print fields_parser.locality_id()
#             print fields_parser.link()
#             print fields_parser.razdel_from_url()
#         item = RealtyItem()
#         fields_parser.populate_item(item)
#         return item        