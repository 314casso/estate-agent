# -*- coding: utf-8 -*-
from estatebase.models import EstateTypeCategory
from exportdata.custom_makers.yaxmlplus import YandexPlusXML, YandexPlusWrapper
from exportdata.utils import EstateTypeMapper

class BnWrapper(YandexPlusWrapper):
    def lot_type(self):        
        estate_type_id = self._basic_stead.estate_type_id if self._basic_stead else None 
        return self.estate_stead_mapper(estate_type_id)
    
    def estate_stead_mapper(self, estate_type_id):
        DEFAULT = u'свободного назначения'
        mapper = {
                  EstateTypeMapper.DACHNYYUCHASTOK : u'ДНП',
                  EstateTypeMapper.UCHASTOKDLYASTROITELSTVADOMA : u'ИЖС',
                  EstateTypeMapper.UCHASTOKSELSKOHOZYAYSTVENNOGONAZNACHENIYA : u'ФЕР',                      
                  EstateTypeMapper.UCHASTOKSELSKOHOZYAYSTVENNOGONAZNACHENIYA : u'ФЕР',
                  EstateTypeMapper.UCHASTOKINOGONAZNACHENIYA : u'ЛПХ',
                  }
            
        if estate_type_id in mapper:
            return mapper[estate_type_id]
        return DEFAULT

class BnXML(YandexPlusXML):
    name = 'bn'
    def __init__(self, bn_wrapper):
        super(BnXML,self).__init__(bn_wrapper)         
