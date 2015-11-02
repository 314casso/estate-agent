# -*- coding: utf-8 -*-
from exportdata.custom_makers.yaxml import YandexXML, YandexWrapper
from estatebase.models import EstateParam
from exportdata.xml_makers import SalesAgent

class IdinaidiWrapper(YandexWrapper):
    pass


class IdinaidiSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-989-769-9952'


class IdinaidiXML(YandexXML):
    name = 'idinaidi'
    def __init__(self, idinaidi_wrapper):
        super(IdinaidiXML,self).__init__(idinaidi_wrapper)
        
    def get_queryset(self):
        q = super(IdinaidiXML,self).get_queryset()
        q = q.filter(estate_params__exact = EstateParam.IDINAIDI)
        return q
        
    def get_sales_agent(self, estate):
        return IdinaidiSalesAgent(estate)