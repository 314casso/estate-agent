# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from realty.utils import process_value_base, join_strings
from urlparse import parse_qs, urlparse
from scrapy.selector import Selector
import re
from realty.fields_parser import BasePhoneImageParser
from estatebase.models import Locality
from exportdata.utils import EstateTypeMapper, LocalityMapper
from scrapy.http import Request
from realty.items import RealtyItem
from selenium import webdriver
from time import sleep
import base64
import md5
from settings import MEDIA_ROOT, STATIC_ROOT
import os
import datetime
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from realty.vector import ImageDecoder, VectorCompare
import subprocess
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87"
)

driver = webdriver.PhantomJS(port=65000, desired_capabilities=dcap)

def login_avito(driver):
    username = "olegpe2000@mail.ru"
    password = "jwtyrf15052014"
    login_url = "https://www.avito.ru/profile/login"    
    driver.get(login_url)    
    WebDriverWait(driver, 30).until(lambda driver : driver.find_element_by_name("login")).send_keys(username)
    WebDriverWait(driver, 30).until(lambda driver : driver.find_element_by_name("password")).send_keys(password)
    WebDriverWait(driver, 30).until(lambda driver : driver.find_element_by_class_name("btn-yellow")).submit()

login_avito(driver)

DECODER_SETTINGS = {
           'avito_phone': {
                            'icons_path': os.path.join(STATIC_ROOT, 'avito_lib'),                            
                            'iconset': ['0','1','2','3','4','5','6','7','8','9','-'],
                            }                     
           }

class AvitoFleldsParser(BasePhoneImageParser): 
    _phone_data = None  
    _breadcrumb = None     
    def __init__(self, *a, **kw):
        self.data = kw.pop('data')
        self.localities = self.data['localities'] 
        self.spider_js = SpyderJS()
        super(AvitoFleldsParser, self).__init__(*a, **kw)
        
    def title_parser(self):
        return self.sel.xpath('//h1[@itemprop="name"]/text()').extract()

    def breadcrumbs_parser(self):
        breadcrumbs = self.sel.xpath('//a[@class="breadcrumb-link"]/text()')
        
        breadcrumb = breadcrumbs[-1].extract().lower()
        return breadcrumb

    def get_breadcrumbs(self):
        if not self._breadcrumb:            
            self._breadcrumb = self.breadcrumbs_parser()
        return self._breadcrumb
                 
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
                         ur'гостиница' : EstateTypeMapper.GOSTINITSA,                                                  
                         ur'офисное' : EstateTypeMapper.OFIS,                         
                         ur'свободного' : EstateTypeMapper.ZDANIE,
                         ur'производственное' : EstateTypeMapper.PROIZVODSTVENNAYABAZA,
                         ur'складское' : EstateTypeMapper.SKLAD,
                         ur'торговое' : EstateTypeMapper.MAGAZIN,                         
                         } 
        txt = self.get_breadcrumbs()
        print u"BREADCRUMBS: %s" % txt        
        if txt:           
            result = self.re_mapper(mapper, txt)
            if callable(result):
                return result()
        return result or self.ZDANIE
        
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
        result = []
        result.append(self.title())
        result.append('\n')
        result.append(join_strings(self.sel.xpath('//div[@itemprop="description"]//text()').extract(), ', '))        
        return result
    
    def price_parser(self):
        return self.sel.xpath('//span[@itemprop="price"]/text()').re(r'\d')
    
    def mesure_parser(self):
        return u'руб.'
    
    def locality_id(self):
        if not self._locality_id:
            self._locality_id = self.locality_parser()            
        return self._locality_id
    
    def get_phone_data(self):
        if not self._phone_data:
            self._phone_data = self.spider_js.decode_phone(self.url)
        return self._phone_data
    
    def phone(self):        
        return [self.get_phone_data()['phone']]
    
    def phone_filename(self):      
        return self.get_phone_data()['filename']
    
    def phone_guess(self):      
        return self.get_phone_data()['guess']

def process_value(value):   
    return process_value_base(value, AvitoSpider.name)


class AvitoSpider(CrawlSpider):
    ORIGIN_ID = 1
    MAX_PAGE = 20 
    _last_page = {}
    name = 'avito'
    allowed_domains = ['avito.ru']
    custom_settings = {'DOWNLOAD_DELAY': 7}
    localities = {
                    'gelendzhik':LocalityMapper.GELENDZHIK,
                    'anapa': LocalityMapper.ANAPA, 
                    'novorossiysk':LocalityMapper.NOVOROSSIYSK, 
                    'temryuk':LocalityMapper.TEMRYUK,                    
                    'abrau-dyurso': LocalityMapper.ABRAUDYURSO,
                    'anapskaya': LocalityMapper.ANAPSKAYA,
                    'arhipo-osipovka': LocalityMapper.ARHIPOOSIPOVKA,
                    'ahtanizovskaya': LocalityMapper.AHTANIZOVSKAYA,
                    'verhnebakanskiy': LocalityMapper.VERHNEBAKANSKIY,
                    'vinogradnyy': LocalityMapper.VINOGRADNYY,
                    'vityazevo': LocalityMapper.VITYAZEVO,
                    'vyshesteblievskaya': LocalityMapper.VYSHESTEBLIEVSKAYA,
                    'gayduk': LocalityMapper.GAYDUK,
                    'glebovka': LocalityMapper.GLEBOVSKOE,
                    'golubitskaya': LocalityMapper.GOLUBITSKAYA,
                    'gostagaevskaya': LocalityMapper.GOSTAGAEVSKAYA,
                    'kurchanskaya': LocalityMapper.KURCHANSKAYA,
                    'kabardinka': LocalityMapper.KABARDINKA,
                    'divnomorskoe': LocalityMapper.DIVNOMORSKOE,
                    'dzhiginka': LocalityMapper.DZHIGINKA,
                    'myshako': LocalityMapper.MYSHAKO,
                    'natuhaevskaya': LocalityMapper.NATUHAEVSKAYA,
                    'raevskaya': LocalityMapper.RAEVSKAYA,
                    'yurovka': LocalityMapper.YUROVKA,
                    'tsibanobalka': LocalityMapper.TSYBANOBALKA,
                    'taman': LocalityMapper.TAMAN,
                    'supseh': LocalityMapper.SUPSEH,
                    'krasnodarskiy_kray_strelka': LocalityMapper.STRELKA,
                    'starotitarovskaya': LocalityMapper.STAROTITAROVSKAYA,
                    'sennoy': LocalityMapper.SENNOY,
                  }  
    rules = (            
        Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="pagination__nav clearfix"]/a',)), follow=True, process_request='process_request_filter', callback='process_response_filter'),
        Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="title"]/h3[@class="h3 fader"]/a',), process_value=process_value), callback='parse_item'),
    )   
       
    def start_requests(self):
        template = "https://www.avito.ru/%s/%s/prodam?user=1&view=list"
        com_template = "https://www.avito.ru/%s/kommercheskaya_nedvizhimost/prodam/%s/za_vse?user=1&view=list"
        urls = []
        
        types = ['kvartiry','komnaty', 'doma_dachi_kottedzhi', 'zemelnye_uchastki', 'garazhi_i_mashinomesta',]
        com_types = ['magazin', 'gostinicy', 'drugoe', 'proizvodstvo', 'sklad', 'ofis']
        for l in self.localities.iterkeys():            
            for t in types:
                urls.append(template % (l, t))                
            for com_type in com_types:
                urls.append(com_template % (l, com_type)) 
        for url in urls:
            print url
            yield Request(url, self.parse)
    
    def parse_item(self, response):
        item = RealtyItem()
        fields_parser = AvitoFleldsParser(Selector(response), response.url, data={'localities': self.localities})
        fields_parser.populate_item(item)        
        item.print_item()
        return item

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
    _full_filename = None
    def __init__(self):
        self.IMAGE_ROOT = os.path.join(MEDIA_ROOT, 'spyder', 'avito')
    
    def get_full_filename(self, url):
        if not self._full_filename:                    
            driver.get(url)
            elem = driver.find_element_by_class_name("js-phone-show__insert")
            if not elem:
                return None
            elem.click()
            sleep(2)
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
            self._full_filename = os.path.join(directory, filename)      
            default_storage.save(self._full_filename, ContentFile(plaindata))
            subprocess.call('convert %s -transparent "#FFFFFF" -alpha background %s' % (self._full_filename, self._full_filename), shell=True)        
        return self._full_filename
        
    def decode_phone(self, url): 
        full_filename = self.get_full_filename(url)
        if not full_filename:
            return {'filename': None, 'guess': 0, 'phone': None}
        image_decoder = ImageDecoder(DECODER_SETTINGS['avito_phone'], VectorCompare())
        result = image_decoder.decode(full_filename)
        guess = result[1]
        phone = ''.join(result[0])        
        return {'filename': full_filename, 'guess': guess, 'phone': phone}                                     
