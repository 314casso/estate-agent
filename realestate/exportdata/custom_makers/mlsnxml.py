# -*- coding: utf-8 -*-
from exportdata.custom_makers.yaxml import YandexXML, YandexWrapper
from estatebase.models import EstateParam
from exportdata.xml_makers import SalesAgent

class MlsnWrapper(YandexWrapper):
    pass


class MlsnSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-989-764-1415'


class MlsnXML(YandexXML):
    name = 'mlsn'
    def __init__(self, mlsn_wrapper):
        super(MlsnXML,self).__init__(mlsn_wrapper)
        
    def get_queryset(self):
        q = super(MlsnXML,self).get_queryset()
        q.filter(estate_params__exact = EstateParam.PAYEXPORT)
        return q
        
    def get_sales_agent(self, estate):
        return MlsnSalesAgent(estate)