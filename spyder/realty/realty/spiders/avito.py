# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
from realty.utils import process_value_base
from urlparse import parse_qs, urlparse
from scrapy.selector import Selector
import re


def process_value(value):                 
    return process_value_base(value, AvitoSpider.name)


class AvitoSpider(CrawlSpider):   
    ORIGIN_ID = 1
    MAX_PAGE = 20 
    _last_page = {}
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = [
                  'http://www.avito.ru/anapa/nedvizhimost?view=list&user=1',
                  'https://www.avito.ru/gelendzhik/nedvizhimost?view=list&user=1',                  
                  ]
           
    rules = (            
        Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="pagination__nav clearfix"]/a',)), follow=True, process_request='process_request_filter', callback='process_response_filter'),
#         Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="title"]/h3[@class="h3 fader"]/a',), process_value=process_value), callback='parse_item'),
    )   

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url, level=log.INFO)                       
#         fields_parser = VdvAnapaFleldsParser(Selector(response), response.url)
#         item = RealtyItem()
#         fields_parser.populate_item(item)
#         return item

    def process_response_filter(self, response):
        print response.url        
        dates = Selector(response).xpath('//span[@class="date"]/text()')
        for date in dates:
            txt = date.extract()
            key = ur'вчера|сегодня'
            matches = re.search(key, txt, re.I | re.U)
            if not matches:
                page_num = self.get_page_num(response.url)
                if page_num:
                    self.set_last_page(response.url, int(page_num))                               
        return []        
    
    def set_last_page(self, url, value):
        path = urlparse(url).path
        self._last_page[path] = value
        
    def get_last_page(self, url):
        path = urlparse(url).path
        return self._last_page.get(path, self.MAX_PAGE) 

    def get_page_num(self, url):        
            qs = parse_qs(urlparse(url).query)
            if 'p' in qs:
                return int(qs['p'][0])
            return 0
        
    def process_request_filter(self, request):      
        if self.get_page_num(request.url) > self.get_last_page(request.url):            
            return None
        return request                           
