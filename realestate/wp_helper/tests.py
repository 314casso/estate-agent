# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from wp_helper.service import WPService
from wp_helper.models import WordpressMeta, WordpressTaxonomyTree
from unittest.case import TestCase
from estatebase.models import Locality

class SimpleTest(TestCase):
    def test_meta(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        #q = WordpressMeta.objects.filter(wordpress_meta_type=WordpressMeta.LOCALITY)
        #return qs.filter(level__lte=2, parent__regions__id=2)
        #q = WordpressTaxonomyTree.objects.all()        
        s = WPService()
#         try:               
        s.delete_taxonomy(1066)
#         except:
#             print 'ERROR'
#         
#         print 'OK!!!!'
        #s = u'\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u0441 \u0443\u043a\u0430\u0437\u0430\u043d\u043d\u044b\u043c \u0438\u043c\u0435\u043d\u0435\u043c \u0443\u0436\u0435 \u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443\u0435\u0442 \u0443 \u0440\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430.'                
        #print s.decode('utf8')
        #self.assertIsNotNone(t, u'Не найден %s' % term)
        #k = 5
        #key = s.get_post_id_by_meta_key(k)     
        #self.assertTrue(key > 0, u'Ключ %s не найден' % k)
        #print key
