from estatebase.models import Estate, EstateParam
from exportdata.xml_makers import SalesAgent
from exportdata.custom_makers.yaxml import YandexXML


class NaydidomXML(YandexXML):
    name = 'naydidom'    
    def get_sales_agent(self, estate):
        return NaydidomSalesAgent(estate)
    
    
class NaydidomSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-918-647-2727'
    
    
class MailruXML(YandexXML):
    name = 'mailru'    
    def get_sales_agent(self, estate):
        return MailruSalesAgent(estate)
    
    
class MailruSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-989-770-6010'    
    
        