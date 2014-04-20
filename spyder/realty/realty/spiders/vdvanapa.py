# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
from realty.fields_parser import BaseFieldsParser
from realty.utils import join_strings, process_value_base
from realty.items import RealtyItem
from estatebase.models import EstateType
from scrapy.selector import Selector

class VdvAnapaFleldsParser(BaseFieldsParser):
    def title_parser(self):
        return self.sel.xpath('//a[@class="bar rubric-l"]/text()').extract()
                 
    def estate_type_parser(self):
        mapper = {
                         ur'гараж' : 9,
                         ur'квартиру' : 6,
                         ur'комнату' : 21,
                         ur'дом' : 16,
                         ur'дача' : 13,
                         ur'коттедж' : 16,
                         ur'участок': 15,
                         ur'коммерческая': self.commerce_parser,
                         ur'гостиница': 12,
                         } 
        txt = self.title()
        parts = txt.split()
        if parts:           
            result = self.re_mapper(mapper, parts[0])
            if callable(result):
                return result()
        return result or self.ZDANIE
    
    def commerce_parser(self):
        COMMERCE_CAT_ID = 6        
        full_txt = join_strings(self.sel.xpath('//div[@class="media-body"]/p[@class="text_justify"]/text()').extract())
        txt = join_strings(full_txt.split()[:3], ' ')   
        print  txt
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
        return self.sel.xpath('//i[@class="icon-phone-sign red_phone"]/../text()').extract()        
    
    def room_count_parser(self): 
        return self.sel.xpath(u'//b[contains(.,"Количество комнат:")]/../text()').extract()
        
    def region_parser(self):
        return self.ANAPA
    
    def locality_parser(self):
        return self.title()
    
    def name_parser(self):
        return [u'неизвестно']
    
    def desc_parser(self):
        result = []
        result.append(self.title())
        result.append('\n')
        result.append(join_strings(self.sel.xpath('//div[@class="media-body"]//text()').extract(), ', '))        
        return result
    
    def price_parser(self):
        return self.sel.xpath('//span[@class="bar price-l"]/text()').re(r'\d')
    
    def mesure_parser(self):
        return u'руб.'
    
    def locality_id(self):
        if not self._locality_id:
            self._locality_id = self.get_locality(field_name='name_loct') 
        return self._locality_id
    
    def phone(self):
        PHONECODE = '86133'
        phones = self.filter_phone()
        if phones:
            return ['8%s%s' % (PHONECODE, phone) if 5 <= len(phone) < 10 else phone for phone in phones]

def process_value(value):            
    return process_value_base(value, VdvApanaSpider.name)

class VdvApanaSpider(CrawlSpider):   
    ORIGIN_ID = 8 
    name = 'vdvanapa'
    allowed_domains = ['vdvanapa.ru']
    start_urls = [
                  'http://vdvanapa.ru/rubricdeal/1/1',
                  'http://vdvanapa.ru/rubricdeal/2/1',
                  'http://vdvanapa.ru/rubricdeal/3/1',
                  'http://vdvanapa.ru/rubricdeal/5/1',
                  'http://vdvanapa.ru/rubricdeal/6/1',
                  'http://vdvanapa.ru/rubricdeal/7/1',
                  ]
           
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//li[@class="next_page"]/a',)), follow=True),
        Rule (SgmlLinkExtractor(restrict_xpaths=('//a[@class="more_link"]',), process_value=process_value), callback='parse_item')
    )   

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url, level=log.INFO)               
        fields_parser = VdvAnapaFleldsParser(Selector(response), response.url)
        item = RealtyItem()
        fields_parser.populate_item(item)
        return item
        
        
        
               
        
    