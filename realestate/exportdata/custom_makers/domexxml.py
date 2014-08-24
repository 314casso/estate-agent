# -*- coding: utf-8 -*-
from estatebase.models import EstateTypeCategory
from exportdata.custom_makers.yaxml import COMMERCE_STEADS, YandexWrapper
from exportdata.custom_makers.yaxmlplus import YandexPlusXML
from exportdata.utils import EstateTypeMapper

class DomexWrapper(YandexWrapper):
    def estate_type(self):        
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE:
            return u'коммерческая'
        if self._basic_stead and self._basic_stead.estate_type_id in COMMERCE_STEADS:
            return u'коммерческая'
        return u'жилая'
    
    def estate_category(self):
        if self._estate.estate_category_id == EstateTypeCategory.COMMERCE and self._basic_bidg:             
            return self.estate_type_com_mapper(self._basic_bidg.estate_type_id) 
        return super(DomexWrapper, self).estate_category()
    
    def estate_type_com_mapper(self, estate_type_id):
        DEFAULT = u'свободного назначения'
        mapper = {
                  EstateTypeMapper.SKLAD : u'склад',
                  EstateTypeMapper.KAFE : u'общепит',
                  EstateTypeMapper.RESTORAN : u'общепит',
                  EstateTypeMapper.TORGOVYYPAVILON : u'торговое помещение',
                  EstateTypeMapper.MAGAZIN : u'торговое помещение',
                  EstateTypeMapper.GOSTINICHNYYKOMPLEKS : u'готовый бизнес',
                  EstateTypeMapper.PROIZVODSTVENNOSKLADSKAYABAZA : u'готовый бизнес',
                  EstateTypeMapper.KONNOSPORTIVNYYKOMPLEKS : u'готовый бизнес',
                  EstateTypeMapper.PROMYSHLENNAYABAZA : u'готовый бизнес',
                  }    
        if estate_type_id in mapper:
            return mapper[estate_type_id]
        return DEFAULT

class DomexXML(YandexPlusXML):
    name = 'domex'
    def __init__(self, domex_wrapper):
        super(DomexXML,self).__init__(domex_wrapper)         
      
    