# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.item import Item
from scrapy import log
import re
from realty.fields_parser import BaseFieldsParser

class VdvAnapaFleldsParser(BaseFieldsParser):
    def title_parser(self):
        return self.sel.xpath('//a[@class="bar rubric-l"]/text()').extract()
                 
    def estate_type_parser(self):
        mapper = {
#                          'garazhi' : 9,
                         ur'квартиру' : 6,
                         ur'комнату' : 21,
                         ur'дом' : 16,
                         ur'дача' : 13,
                         ur'коттедж' : 16,
#                         ur'участок': self.stead_parser,
                         ur'офис': 35,
                         ur'склад': 53,
#                         'kommercheskaya-nedvizhimost' : 93,
                         } 
        txt = self.title
        parts = txt.split()
        if parts:           
            result = self.re_mapper(mapper, parts[0])
            if callable(result):
                return result()
        return result or self.ZDANIE
    
    def phone_parser(self): pass        
    
    def room_count_parser(self): pass
        
    def region_parser(self): pass
    
    def locality_parser(self): pass
    
    def name_parser(self): pass
    
    def desc_parser(self): pass
    
    def price_parser(self): pass
    
    def mesure_parser(self): pass

class LiferealtySpider(CrawlSpider):    
    name = 'vdvanapa'
    allowed_domains = ['vdvanapa.ru']
    start_urls = ['http://vdvanapa.ru/rubricdeal/1/1']

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//li[@class="next_page"]/a',)), follow=True),
        Rule (SgmlLinkExtractor(restrict_xpaths=('//a[@class="more_link"]',)), callback='parse_item')
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url, level=log.INFO)       
        fields_parser = VdvAnapaFleldsParser(response)
        print fields_parser.estate_type_id
        
               
        
    