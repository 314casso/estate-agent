# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy import log
from scrapy.http import Request
import re
from realty.utils import join_strings
from realty.items import RealtyItem

class LiferealtySpider(CrawlSpider):
    name = 'liferealty'
    ORIGIN_ID = 3
    allowed_domains = ['krasnodar.life-realty.ru']
    start_urls = [
                  'http://krasnodar.life-realty.ru/sale/?view=simple&searchStreet=0&streetText=&inputStreet=&c%5B%5D=1&c%5B%5D=4&c%5B%5D=7&r%5B%5D=47&c%5B%5D=1&c%5B%5D=1219&c%5B%5D=624&c%5B%5D=1579&c%5B%5D=1229&c%5B%5D=1028&c%5B%5D=1369&c%5B%5D=1237&c%5B%5D=1627&c%5B%5D=930&c%5B%5D=1424&c%5B%5D=1023&c%5B%5D=1976&c%5B%5D=1528&c%5B%5D=693&c%5B%5D=1052&c%5B%5D=959&c%5B%5D=1027&c%5B%5D=1226&c%5B%5D=994&r%5B%5D=46&c%5B%5D=187&c%5B%5D=1585&c%5B%5D=4&c%5B%5D=690&c%5B%5D=691&c%5B%5D=1225&r%5B%5D=43&c%5B%5D=1067&c%5B%5D=1127&c%5B%5D=1098&c%5B%5D=7&c%5B%5D=1511&r%5B%5D=31&c%5B%5D=114&c%5B%5D=361&c%5B%5D=594&c%5B%5D=115&c%5B%5D=414&c%5B%5D=243&c%5B%5D=358&c%5B%5D=119&c%5B%5D=195&c%5B%5D=120&c%5B%5D=1022&c%5B%5D=1795&c%5B%5D=121&c%5B%5D=122&c%5B%5D=1244&c%5B%5D=425&c%5B%5D=354&c%5B%5D=279&c%5B%5D=124&c%5B%5D=193&c%5B%5D=275&c%5B%5D=923&c%5B%5D=125&c%5B%5D=126&c%5B%5D=924&c%5B%5D=1209&priceFrom=&priceTo=&areaTotalFrom=&areaTotalTo=&areaLivingFrom=&areaLivingTo=&areaRoomFrom=&areaRoomTo=&floorTotalFrom=&floorTotalTo=&floorFrom=&floorTo=&page=1',
                  'http://krasnodar.life-realty.ru/country/?view=simple&offerId=&agencyOfferId=&searchPhone=&searchFio=&searchStreet=0&streetText=&inputStreet=&c%5B%5D=1&c%5B%5D=4&c%5B%5D=7&r%5B%5D=47&c%5B%5D=1&c%5B%5D=1219&c%5B%5D=624&c%5B%5D=1341&c%5B%5D=1579&c%5B%5D=1229&c%5B%5D=1028&c%5B%5D=1237&c%5B%5D=1627&c%5B%5D=930&c%5B%5D=1424&c%5B%5D=1023&c%5B%5D=2919&c%5B%5D=919&c%5B%5D=1976&c%5B%5D=693&c%5B%5D=1052&c%5B%5D=1953&c%5B%5D=959&c%5B%5D=1027&c%5B%5D=1226&c%5B%5D=994&r%5B%5D=46&c%5B%5D=2099&c%5B%5D=187&c%5B%5D=1585&c%5B%5D=2355&c%5B%5D=4&c%5B%5D=1159&c%5B%5D=690&c%5B%5D=691&c%5B%5D=1138&c%5B%5D=981&c%5B%5D=1225&r%5B%5D=43&c%5B%5D=3341&c%5B%5D=593&c%5B%5D=3134&c%5B%5D=1067&c%5B%5D=3400&c%5B%5D=1127&c%5B%5D=3378&c%5B%5D=3315&c%5B%5D=1098&c%5B%5D=360&c%5B%5D=7&c%5B%5D=986&c%5B%5D=1956&c%5B%5D=3253&c%5B%5D=1994&c%5B%5D=3312&c%5B%5D=1511&c%5B%5D=1615&c%5B%5D=1397&r%5B%5D=31&c%5B%5D=114&c%5B%5D=361&c%5B%5D=594&c%5B%5D=286&c%5B%5D=115&c%5B%5D=414&c%5B%5D=117&c%5B%5D=644&c%5B%5D=243&c%5B%5D=358&c%5B%5D=119&c%5B%5D=195&c%5B%5D=962&c%5B%5D=120&c%5B%5D=1022&c%5B%5D=1795&c%5B%5D=121&c%5B%5D=122&c%5B%5D=123&c%5B%5D=425&c%5B%5D=354&c%5B%5D=279&c%5B%5D=124&c%5B%5D=554&c%5B%5D=193&c%5B%5D=275&c%5B%5D=923&c%5B%5D=125&c%5B%5D=126&c%5B%5D=924&c%5B%5D=1209&priceFrom=&priceTo=&areaTotalFrom=&areaTotalTo=&areaLivingFrom=&areaLivingTo=&areaPlotFrom=&areaPlotTo=&page=1',
                  ]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@id="nextPage"]',)), follow=True, callback='parse_item'),
    )

    def parse_item(self, response):       
        sel = Selector(response)
        if 'detail_page' in response.meta:
            saler_type = join_strings(sel.xpath('//div[@class="c_face"]/span[@class="lgrey"]/text()').extract())
            if self.check_saler_type(saler_type):                           
                address = join_strings(sel.xpath('//*[@id="list_sale"]/div[@class="card_block"][1]/text()').extract(), ', ')            
                name = join_strings(sel.xpath('//div[@class="c_face"]/text()').extract())              
                phone_str = join_strings(join_strings(sel.xpath('//div[@class="c_phone"]/text()').extract()))
                page_title = join_strings(sel.xpath('//*[@id="list_sale"]/h1/text()').extract())
                description = join_strings(sel.xpath('//*[@id="list_sale"]/div[@class="card_block"]/text()').extract(), '\n')
                print(description)
                price = join_strings(sel.xpath('//div[@class="card_price"]/text()').extract())
                mesure = join_strings(sel.xpath('//div[@class="card_price"]/span/text()').extract())                
                item = RealtyItem()
                item['phone'] = self.filter_phone(phone_str)         
                item['name'] = [name]
                item['desc'] = [description]            
                item['price'] = ['%s %s' % (price, mesure)]
                item['price_digit'] = [self.get_digit_price(price, mesure)]
                item['link'] = [response.url]
                item['estate_type_id'] = self.estate_type_parser(page_title)                         
                item['region_id'] = self.region_parser(address)            
                #item['locality'] = ''
                #item['microdistrict'] = ''
                #item['street'] = ''
                #item['estate_number'] = ''
                item['room_count'] = self.room_count_parser(page_title)
                yield item        
        rows = sel.xpath('//tr[@offerid]')
        for tr in rows:
            vip_an = tr.xpath('td/div/div[@class="vip_an"]')            
            
            if not vip_an:
                links = tr.xpath('td[@class="txt"]/a[@offerid]/@href').extract()
                for url in links:                    
                    yield Request(url, callback=self.parse_item, meta={'detail_page':True})
    
    def check_saler_type(self, txt):
        mapper = {
                       ur'собственник' : 1,
                 }
        return self.re_mapper(mapper, txt) 
        
    def room_count_parser(self, txt):
        mapper = {
                    ur'однокомнатная' : 1,
                    ur'двухкомнатная' : 2,
                    ur'трехкомнатная' : 3,
                    ur'четырехкомнатная' : 4,                    
                 }
        return self.re_mapper(mapper, txt)
        
    def region_parser(self, txt):        
        mapper = {
                    ur'пункт: Анапа' : 1,
                    ur'пункт: Геленджик' : 2,
                    ur'пункт: Новороссийск' : 3,
                    ur'пункт: Темрюкский' : 4,                    
                 }
        return self.re_mapper(mapper, txt)    
        
    def estate_type_parser(self, txt):
        mapper = {
#                          'garazhi' : 9,
#                          'doma' : 16,
#                          'zemelnyie-uchastki' : 15, 
#                          '1-komn-kv' : 6,
#                          '2-komn-kv' : 6,
#                          '3-komn-kv' : 6,
                         ur'квартира' : 6,
                         ur'комната' : 21,
                         ur'дом' : 16,
                         ur'дача' : 13,
                         ur'коттедж' : 22,
#                         'kommercheskaya-nedvizhimost' : 93,
                         }  
        return self.re_mapper(mapper, txt)
    
    def re_mapper(self, mapper, txt):
        for key, value in mapper.iteritems():
            matches = re.search(key, txt, re.I | re.U)            
            if matches:
                return value
    
    def get_digit_price(self, price, mesure):
        mesures = {u'тыс. руб.':1000}
        if price:
            if mesure in mesures:
                price_digit = float(price)
                price_digit = int(price_digit * mesures[mesure])                
                return price_digit
        return 0        
    
    def filter_phone(self, phone_str):
        phones = phone_str.split(',')
        result = []
        for phone in phones:         
            phone = phone.strip().replace('+7', '8')
            result.append(re.sub('\D','', phone))
        return result