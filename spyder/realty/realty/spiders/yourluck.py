# -*- coding: utf-8 -*-
from scrapy import log
from realty.fields_parser import BaseFieldsParser
from realty.utils import join_strings
from realty.items import RealtyItem
from estatebase.models import EstateType, Locality
from scrapy.selector import Selector
from scrapy.http import Request
import re
import urlparse
from scrapy.spider import BaseSpider

class YourLuckFleldsParser(BaseFieldsParser):
    _razdel = None
    def title_parser(self):
        title = join_strings(self.sel.xpath('b/text()').extract())                             
        txt = join_strings(self.sel.xpath('text()').extract(), ' ')            
        txt = join_strings(txt.split()[0:3],' ')        
        title = u'%s %s' % (title, txt)
        return title 
                  
    def razdel_from_url(self):
        if 'section_id' in self.meta:
            return self.meta['section_id']
        return None
                         
    def estate_type_parser(self):        
        razdel_map = {
                      '33': u'коммерческая',
                      }
        mapper = {
                         ur'гараж' : 9,
                         ur'квартир' : 6,
                         ur'ком\.кв' : 6,
                         ur'комнат' : 21,
                         ur'дома|коттедж|танхаус|таунхаус' : 39,
                         ur'дуплекс': 125,
                         ur'дом|домо|хату' : 16,                         
                         ur'часть' : 18,
                         ur'дачу' : 13,
                         ur'домик' : 13,
                         ur'коттедж\b' : 22,
                         ur'участ': 15,
                         ur'пай': 15,
                         ur'коммерческая': self.commerce_parser,                        
                         }        
        txt = razdel_map[self.razdel_from_url()] if self.razdel_from_url() in razdel_map else self.title()
        txt = re.sub(ur'\d|\/',' ', txt)       
        result = self.re_mapper(mapper, txt)
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
        matches = re.search(ur'(\d)\-КОМ', self.title(), re.U | re.I)
        if matches:
            return matches.group(0)
        
    def link(self):
        import hashlib
        id_instead_link = hashlib.md5(join_strings(self.sel.xpath('text()').extract()).encode('utf-8')).hexdigest()
        return [id_instead_link]
        
    def region_parser(self):
        if self.locality_id:
            return Locality.objects.get(pk=self.locality_id).region_id
        return self.ANAPA
    
    def locality_parser(self):
        return self.meta['section']         
    
    def name_parser(self):
        return [u'неизвестно']
    
    def desc_parser(self):
        result = []        
        title = self.sel.xpath('b/text()').extract()
        if title: 
            result.append(join_strings(title).lower().capitalize())        
        result.append(join_strings(self.sel.xpath('text()').extract(), ', '))                
        return [join_strings(result, ' ')]
    
    def price_parser(self):
        return self.sel.re(ur'\d[\d|\.]{3,}\sруб.')
    
    def mesure_parser(self):
        return u'руб.'
    
    def locality_id(self):
        ANAPA_ID = 3 
        if not self._locality_id:
            self._locality_id = self.get_locality() 
            if not self._locality_id:
                self._locality_id = self.get_locality(field_name='name_loct')                
        return self._locality_id or ANAPA_ID
    
    def phone(self):
        PHONECODE = '86133'
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

class YourLuckSpider(BaseSpider):   
    ORIGIN_ID = 7
    name = 'yourluck'
    allowed_domains = ['yourluck.ru']
    start_urls = [     
                  'http://yourluck.ru/luck/archive/',                                           
                  ]
    allowed_cats = ['33','34','35','08']   
    
    def cat_id(self, url):        
        o = urlparse.urlparse(url)           
        return [x for x in o.path.split('/') if x][-1] or None
    
    def parse(self, response):
        '''Parse main page and extract categories links.'''
        sel = Selector(response)
        urls = sel.xpath('//div[@class="arch_sections"]/*/a/@href').extract()
        for url in urls: 
            if self.cat_id(url) in self.allowed_cats:
                url = urlparse.urljoin(response.url, url)            
                yield Request(url, callback = self.parse_page)
        
    def parse_page(self, response):
        for item in self.parse_item(response):
            yield item 
        sel = Selector(response)        
        urls = sel.xpath('//div[@class="pages"]/a/@href').extract()       
        for url in urls:            
            url = urlparse.urljoin(response.url, url)         
            yield Request(url, callback = self.parse_item)
    
    def process_section(self, section):
        PATERN = u'Продаю'        
        txt = join_strings(section.xpath("text()").extract())         
        chains = [x.strip() for x in txt.split(u"→")]
        result = {'sale':False, 'section':None}
        if PATERN in chains:
            result['sale'] = True   
            result['section'] = join_strings(chains, ' ')            
        return result
       
    def parse_item(self, response):        
        self.log('ITEM page! %s' % response.url, level=log.INFO)        
        sel = Selector(response)        
        sections = sel.xpath("//div[@class='board_section']")
        for section in sections:
            parsed_section = self.process_section(section)
            if not parsed_section['sale']:
                continue 
            entries = section.xpath("following-sibling::div[@class='board_notice']")
            meta = {'section':parsed_section['section'], 'section_id':self.cat_id(response.url)}            
            for entry in entries:
                fields_parser = YourLuckFleldsParser(entry, response.url, meta)
                item = RealtyItem()
                fields_parser.populate_item(item)                        
                yield item          