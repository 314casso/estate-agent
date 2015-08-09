# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
from realty.utils import process_value_base, join_strings
from urlparse import parse_qs, urlparse
from scrapy.selector import Selector
import re
from realty.fields_parser import BaseFieldsParser
from estatebase.models import EstateType, Locality
from exportdata.utils import EstateTypeMapper, LocalityMapper
from scrapy.http import Request
from realty.items import RealtyItem
from selenium import webdriver
from time import sleep
import StringIO
from PIL import Image
import base64
import md5
from settings import MEDIA_ROOT, STATIC_ROOT
import os
import datetime
import cStringIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from realty.vector import ImageDecoder, VectorCompare
import subprocess

DECODER_SETTINGS = {
           'avito_phone': {
                            'icons_path': os.path.join(STATIC_ROOT, 'avito_lib'),                            
                            'iconset': ['0','1','2','3','4','5','6','7','8','9','-'],
                            }                     
           }

class AvitoFleldsParser(BaseFieldsParser):    
    def __init__(self, *a, **kw):
        self.localities = kw.pop('localities')
        super(AvitoFleldsParser, self).__init__(*a, **kw)
        
    def title_parser(self):
        return self.sel.xpath('//h1[@itemprop="name"]/text()').extract()

    def breadcrumbs_parser(self):
        a = self.sel.xpath('//a[@class="breadcrumb-link"]/text()')
        breadcrumbs = [x.lower() for x in a.extract()]
        return breadcrumbs

    def get_breadcrumbs(self):
        return join_strings(self.breadcrumbs_parser())
                 
    def estate_type_parser(self):
        mapper = {
                  
                         ur'вторичка' : EstateTypeMapper.KVARTIRA,
                         ur'cтудии' : EstateTypeMapper.KVARTIRASTUDIYA,
                         ur'новостройки' : EstateTypeMapper.NOVOSTROYKA,
                         ur'комнаты' : EstateTypeMapper.KOMNATA,
                         ur'дачи' : EstateTypeMapper.DACHA,
                         ur'дома' : EstateTypeMapper.DOM,
                         ur'коттеджи' : EstateTypeMapper.KOTTEDZH,
                         ur'таунхаусы': EstateTypeMapper.TAUNHAUS,
                         ur'поселений': EstateTypeMapper.UCHASTOKDLYASTROITELSTVADOMA,
                         ur'сельхозназначения': EstateTypeMapper.UCHASTOKSELSKOHOZYAYSTVENNOGONAZNACHENIYA,
                         ur'промназначения': EstateTypeMapper.UCHASTOKINOGONAZNACHENIYA,
                         ur'коммерческая': self.commerce_parser,                         
                         } 
        txt = self.get_breadcrumbs()        
        if txt:           
            result = self.re_mapper(mapper, txt)
            if callable(result):
                return result()
        return result or self.ZDANIE
    
    def commerce_parser(self):
        return self.ZDANIE
#         COMMERCE_CAT_ID = 6        
#         full_txt = join_strings(self.sel.xpath('//div[@class="media-body"]/p[@class="text_justify"]/text()').extract())
#         txt = join_strings(full_txt.split()[:3], ' ')   
#         print  txt
#         key = 'commerce_mapper_smart'  
#         from django.core.cache import cache
#         mapper = cache.get(key)
#         if not mapper:                                
#             types = EstateType.objects.filter(estate_type_category_id=COMMERCE_CAT_ID) 
#             mapper = {}
#             for t in types:
#                 mapper[ur'%s\s' % t.name] = t.id
#                 mapper[ur'%s\s' % t.name_accs] = t.id
#             cache.set(key, mapper, 3600)  
#         return self.re_mapper(mapper, txt) or self.ZDANIE 
    
    def phone_parser(self): 
        return self.sel.xpath('//i[@class="icon-phone-sign red_phone"]/../text()').extract()        
    
    def room_count_parser(self):
        title = self.title()
        m = re.search(ur'(?P<room_cnt>\d)\-к', title, re.I | re.U)
        if m:
            return m.group('room_cnt')  
        
    def region_parser(self):
        return Locality.objects.get(pk=self.locality_id).region_id
    
    def locality_parser(self):
        parse_object = urlparse(self.url)
        parts = parse_object.path.split('/')           
        for part in parts:
            l = self.localities.get(part)
            if l:
                return l 
    
    def name_parser(self):
        return self.sel.xpath('//div[@itemprop="seller"]/strong[@itemprop="name"]/text()').extract()  
    
    def desc_parser(self):
        return "DESC"
        result = []
        result.append(self.title())
        result.append('\n')
        result.append(join_strings(self.sel.xpath('//div[@class="media-body"]//text()').extract(), ', '))        
        return result
    
    def price_parser(self):
        return self.sel.xpath('//span[@itemprop="price"]/text()').re(r'\d')
    
    def mesure_parser(self):
        return u'руб.'
    
    def locality_id(self):
        if not self._locality_id:
            self._locality_id = self.locality_parser()            
        return self._locality_id
    
    def phone(self):
        PHONECODE = '86133'
        phones = self.filter_phone()
        if phones:
            return ['8%s%s' % (PHONECODE, phone) if 5 <= len(phone) < 10 else phone for phone in phones]

def process_value(value):   
    return process_value_base(value, AvitoSpider.name)


class AvitoSpider(CrawlSpider):
    ORIGIN_ID = 1
    MAX_PAGE = 20 
    _last_page = {}
    name = 'avito'
    allowed_domains = ['avito.ru']
    localities = {'gelendzhik':LocalityMapper.GELENDZHIK,}
    #start_urls = [
#                   'http://www.avito.ru/anapa/nedvizhimost?view=list&user=1',
#                   'https://www.avito.ru/gelendzhik/kvartiry/prodam?view=list&user=1', 
#                   'https://www.avito.ru/gelendzhik/komnaty/prodam?user=1&view=list',                 
#                   ]
           
    rules = (            
        Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="pagination__nav clearfix"]/a',)), follow=True, process_request='process_request_filter', callback='process_response_filter'),
        Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="title"]/h3[@class="h3 fader"]/a',), process_value=process_value), callback='parse_item'),
    )   
       
    def start_requests(self):
        template = "https://www.avito.ru/%s/%s/prodam?user=1&view=list"
        urls = []
        
        types = ['kvartiry',]# 'komnaty', 'doma_dachi_kottedzhi', 'zemelnye_uchastki', 'garazhi_i_mashinomesta', 'kommercheskaya_nedvizhimost']
        for l in self.localities.iterkeys():            
            for t in types:
                urls.append(template % (l, t))
        for url in urls:
            yield Request(url, self.parse)
    
    def parse_item(self, response):
        item = RealtyItem()
        fields_parser = AvitoFleldsParser(Selector(response), response.url, localities=self.localities)
        spyder_js = SpyderJS()
        fields_parser.populate_item(item)        
        spyder_js.populate_item(item)            
        item.print_item()
#         return item

    def process_response_filter(self, response):
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
    

class SpyderJS(object):
    def __init__(self):
        self.IMAGE_ROOT = os.path.join(MEDIA_ROOT, 'spyder', 'avito')
    
    def save_phone_image(self, url):
        driver = webdriver.PhantomJS()        
        driver.get(url)
        elem = driver.find_element_by_class_name("js-phone-show__insert")
        elem.click()
        sleep(1)
        res = driver.execute_script("""
          var phone_imgs = document.getElementsByClassName("description__phone-img");
          var canvas = document.createElement("canvas");
          canvas.width = 102;
          canvas.height = 16;
          var ctx = canvas.getContext("2d");          
          ctx.drawImage(phone_imgs[0], 0, 0);
          return canvas.toDataURL("image/png").split(",")[1];
        """)
       
        plaindata = base64.b64decode(res)
        today = datetime.date.today()
        directory = os.path.join(self.IMAGE_ROOT, today.strftime('%d%m%Y'))
        if not os.path.exists(directory):
            os.makedirs(directory)        
        filename = '%s.png' %  md5.new(url).hexdigest()
        full_filename = os.path.join(directory, filename)      
        default_storage.save(full_filename, ContentFile(plaindata))
        subprocess.call('convert %s -transparent "#FFFFFF" -alpha background %s' % (full_filename, full_filename), shell=True)        
        return full_filename
    
    def populate_item(self, item):
        phone_filename = self.save_phone_image(item['link'][0])         
        item['phone_filename'] = phone_filename 
        item['phone'] = [self.decode_phone(phone_filename)]
        
    def decode_phone(self, phone_filename): 
        image_decoder = ImageDecoder(DECODER_SETTINGS['avito_phone'], VectorCompare())
        result = image_decoder.decode(phone_filename)
        if result[1] == 1:
            return ''.join(result[0])                            
