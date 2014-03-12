# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.item import Item
from scrapy import log
from scrapy.http import Request
import re


class LiferealtySpider(CrawlSpider):
    name = 'liferealty'
    allowed_domains = ['krasnodar.life-realty.ru']
    start_urls = ['http://krasnodar.life-realty.ru/sale/?view=simple&searchStreet=0&streetText=&inputStreet=&c%5B%5D=1&c%5B%5D=4&c%5B%5D=7&r%5B%5D=47&c%5B%5D=1&c%5B%5D=1219&c%5B%5D=624&c%5B%5D=1579&c%5B%5D=1229&c%5B%5D=1028&c%5B%5D=1369&c%5B%5D=1237&c%5B%5D=1627&c%5B%5D=930&c%5B%5D=1424&c%5B%5D=1023&c%5B%5D=1976&c%5B%5D=1528&c%5B%5D=693&c%5B%5D=1052&c%5B%5D=959&c%5B%5D=1027&c%5B%5D=1226&c%5B%5D=994&r%5B%5D=46&c%5B%5D=187&c%5B%5D=1585&c%5B%5D=4&c%5B%5D=690&c%5B%5D=691&c%5B%5D=1225&r%5B%5D=43&c%5B%5D=1067&c%5B%5D=1127&c%5B%5D=1098&c%5B%5D=7&c%5B%5D=1511&r%5B%5D=31&c%5B%5D=114&c%5B%5D=361&c%5B%5D=594&c%5B%5D=115&c%5B%5D=414&c%5B%5D=243&c%5B%5D=358&c%5B%5D=119&c%5B%5D=195&c%5B%5D=120&c%5B%5D=1022&c%5B%5D=1795&c%5B%5D=121&c%5B%5D=122&c%5B%5D=1244&c%5B%5D=425&c%5B%5D=354&c%5B%5D=279&c%5B%5D=124&c%5B%5D=193&c%5B%5D=275&c%5B%5D=923&c%5B%5D=125&c%5B%5D=126&c%5B%5D=924&c%5B%5D=1209&priceFrom=&priceTo=&areaTotalFrom=&areaTotalTo=&areaLivingFrom=&areaLivingTo=&areaRoomFrom=&areaRoomTo=&floorTotalFrom=&floorTotalTo=&floorFrom=&floorTo=&page=1']

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@id="nextPage"]',)), follow=True, callback='parse_item'),
    )

    def parse_item(self, response):       
        self.log('Hi, this is an item page! %s' % response.url, level=log.INFO)        
        sel = Selector(response)
        if 'detail_page' in response.meta:
            #/div[@class="c_face"]
            #contacts = sel.xpath('//div[@class="card_contacts"]')
            
            #//*[@id="list_sale"]/div[5]
            #//*[@id="list_sale"]/div[6]
            
            bld_condition = sel.xpath('//*[@id="list_sale"]/div[5]').re(ur'Состояние дома\:\s+(.+)\<br\>')
            self.log('bld_condition! %s' % ''.join(bld_condition), level=log.INFO)
            estate_type = ''.join(sel.xpath('//*[@id="list_sale"]/h1/text()').extract())
            self.log('estate_type! [%s]' % estate_type.strip(), level=log.INFO) 
            description = sel.xpath('//*[@id="list_sale"]/div[4]/text()').extract()
            price = sel.xpath('//div[@class="card_price"]/text()').extract()
            mesure = sel.xpath('//div[@class="card_price"]/span/text()').extract()
            
            self.log('Description! %s' % ''.join(description), level=log.INFO)
            self.log('Price! %s' % ''.join(price) + ''.join(mesure), level=log.INFO)
            #self.log('Contact! %s' % ''.join(contacts.extract()), level=log.INFO)        
        rows = sel.xpath('//tr[@offerid]')
        for tr in rows:
            vip_an = tr.xpath('td/div/div[@class="vip_an"]')            
            
            if not vip_an:
                links = tr.xpath('td[@class="txt"]/a[@offerid]/@href').extract()
                for url in links:                    
                    yield Request(url, callback=self.parse_item, meta={'detail_page':True})
               
        
    def estate_type_parser(self, type_str, item):
        estate_types = {
#                          'garazhi' : 9,
#                          'doma' : 16,
#                          'zemelnyie-uchastki' : 15, 
#                          '1-komn-kv' : 6,
#                          '2-komn-kv' : 6,
#                          '3-komn-kv' : 6,
                         ur'Вторичное' : 6,
                         'komnatyi' : 21,
                         ur'Новостройка' : 34,
                         'kommercheskaya-nedvizhimost' : 93,
                         }  
#         for
#         matches = re.search(, , re.I | re.U)
#         print matches
#         if matches:
                       
    def process_item(self, item):
        pass
        
            
                    
               
            

