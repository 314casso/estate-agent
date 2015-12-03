from exportdata.custom_makers.avitoxml import AvitoXML
from exportdata.xml_makers import SalesAgent
from exportdata.custom_makers.avitopayxml import AvitoXMLPay

    
class GdeetotdomXML(AvitoXML):
    name = 'gdeetotdom'
    def get_sales_agent(self, estate):
        return GdeetotdomSalesAgent(estate)


class GdeetotdomSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-988-669-3067'    
    
    
class KvadroomXML(AvitoXMLPay):
    name = 'kvadroom'
    def get_sales_agent(self, estate):
        return KvadroomSalesAgent(estate)


class KvadroomSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-989-766-7820'
    
    
class UbuXML(AvitoXMLPay):
    name = 'ubu'
    def get_sales_agent(self, estate):
        return UbuSalesAgent(estate)


class UbuSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-988-131-8162'                    