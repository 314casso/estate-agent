# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from wp_helper.service import WPService
from wp_helper.models import WordpressMeta, WordpressTaxonomyTree
from unittest.case import TestCase
from estatebase.models import Locality, Estate
from settings import WP_PARAMS
from django.template.base import Template
from django.template.context import Context
import re

class SimpleTest(TestCase):
    def test_meta(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        
        wp_service = WPService(WP_PARAMS['local'])
        estate = Estate.objects.get(pk=86606) #86606
         
        print wp_service.render_post_title(estate)
        print wp_service.render_seo_post_title(estate)
        for item in  wp_service.render_post_tags(estate):
            print item

        print '='*20
        #print wp_service.render_post_body(estate)
        wp_service.render_post_images(estate)        
              
#         import pymorphy2
#         morph = pymorphy2.MorphAnalyzer()
#                
#                
#         for item in morph.parse(u'Кучугуры'):
#             print item.normal_form
#             #if item.normal_form == item.word and item.tag.animacy == 'inan' or item.tag.animacy is None:    
#             print item.inflect({'loct'}).word 
           
          
#         print morph.parse(u'Ханчакрак')[0].inflect({'sing', 'loct'}).word
#         
#         print morph.parse(u'квартира')[0].inflect({'sing', 'accs'}).word
             
        #print s.inflect('Голубицкая',6)
        #print s.get_post_id_by_meta_key(69225)
        #category =  s.get_or_create_category(3, u'дача')
        #if category is not None:
        #    print category.wp_id
 
#   def inflect(self, name, case):
#         from hashlib import sha1
#         from django.core.cache import cache
#         cache_key = sha1('inflect_cache_%s_%s' % (name, case)).hexdigest()
#         result = cache.get(cache_key)        
#         if result:                         
#             return result 
#         import urllib
#         from xml.etree import ElementTree
#         url = 'http://export.yandex.ru/inflect.xml?'
#         url += urllib.urlencode([('name', name.encode('utf-8'))])
#         response = urllib.urlopen(url)
#         tree = ElementTree.parse(response)
#         elem = tree.find( './/inflection[@case="%s"]' % case)                
#         if elem is not None:
#             cache.set(cache_key, elem.text)            
#             return elem.text
            
