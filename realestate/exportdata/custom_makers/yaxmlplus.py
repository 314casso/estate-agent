# -*- coding: utf-8 -*-
from estatebase.models import Estate, EstateTypeCategory
from exportdata.custom_makers.yaxml import YandexWrapper, YandexXML,\
    COMMERCE_STEADS

class YandexPlusWrapper(YandexWrapper):
    def estate_type(self):        
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE:
            return u'коммерческая'
        if self._basic_stead and self._basic_stead.estate_type_id in COMMERCE_STEADS:
            return u'коммерческая'
        return u'жилая'
    
    def estate_category(self):
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE and self._basic_bidg:
            result = u'%s' % self._basic_bidg.estate_type
            return result.lower() 
        return super(YandexPlusWrapper, self).estate_category()

class YandexPlusXML(YandexXML):
    name = 'yaxmlplus'
    def __init__(self, yandex_plus_wrapper):
        super(YandexPlusXML,self).__init__(yandex_plus_wrapper)         
        
    def get_queryset(self):
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),             
             'agency_price__gte': MIN_PRICE_LIMIT,             
             }
        q = Estate.objects.all()
        q = q.filter(**f)        
        q = q.exclude(street__name__exact = u'без улицы')        
        return q