# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from realty.items import RealtyItem
from scrapy.contrib.loader.processor import MapCompose
import re

class SlrgelSpider(BaseSpider):
    name = "slrgel"
    origin_id = 13
    allowed_domains = ["slrgel"]    
    start_urls = [
        "http://slrgel.ru/category/garazhi/",
        #"http://slrgel.ru/category/doma/",
        #'http://slrgel.ru/category/zemelnyie-uchastki/',
        #'http://slrgel.ru/category/kvartiryi/1-komn-kv/'
    ]

    def parse(self, response):
        proc_phone = MapCompose(self.filter_phone)        
        proc_price = MapCompose(self.filter_price)
        sel = Selector(response)
        sites = sel.xpath("//div[@class='t1 tab']/article")       
        items = []
        for site in sites:           
            item = RealtyItem()           
            item['phone'] = proc_phone(site.xpath("div/div/span[@class='phone']/text()").re(r'(?:[\+\d]|[\d])+[\d|\-|\s]*'))         
            item['name'] = site.xpath("div/div/span[@class='phone']/text()").re(r'\,\s+(\D+)$')
            item['desc'] = site.xpath("div[@class='entry-content']/p/text()").extract()            
            item['price'] = site.xpath("div/div/span[@class='price']/text()").extract()
            item['price_digit'] = proc_price(site.xpath("div/div/span[@class='price']/text()").extract())
            item['link'] = site.xpath("div/h2[@class='entry-title']/a/@href").extract()
            item['estate_type'] = self.get_estate_type(response.url)                         
            items.append(item)
        return items
      
    def filter_phone(self, phone):
        phone = phone.replace('-', '')
        return '8%s' % phone   
       
    def filter_price(self, price):
        mesures = {u'т.р.':1000, u'млн.р.':1000000}
        if price:            
            m = re.search(r'(?P<digit>\d+[\d|\,]*)\s(?P<mesure>[\w|\.]+)', price, re.UNICODE)
            if m:                
                price_digit = float(m.group('digit').replace(',','.'))
                price_digit = int(price_digit * mesures[m.group('mesure')])                
                return price_digit
   
    def get_estate_type(self, url):
        m = re.search(r'\/(?P<key>[^\/]+)[\/]{0,1}$', url)
        if m:
            key = m.group()
            estate_types = {
                         'garazhi' : 7,
                         'doma' : 16,
                         'zemelnyie-uchastki' : 15, 
                         '1-komn-kv' : 6,
                         }            
            if key in estate_types:
                return estate_types[key]
