# -*- coding: utf-8 -*-
import unittest
from realty.spiders.slrgel import SlrgelSpider
from realty.pipelines import RealtyPipeline
from realty.items import RealtyItem

class RealtyPipelineTest(unittest.TestCase):

    def setUp(self):
        self.spider = SlrgelSpider()
        self.pipe = RealtyPipeline() 
        self.item = RealtyItem()
        self.item['phone'] = ['77777777777']    
        self.item['desc'] = ['TEST_DESC']
        self.item['name'] = ['TEST_CLIENT']
        self.item['price'] = ['1 млн.р.']
        self.item['price_digit'] = ['1000000'] 
        self.item['link'] = ['http://test-spyder-link.ru']
        self.item['estate_type'] = 16               
    
    def test_parse(self):
        self.pipe.process_item(self.item, self.spider)
        #self.assertEqual(1, 0) 