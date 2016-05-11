from exportdata.custom_makers.avitoxml import AvitoXML
from exportdata.xml_makers import SalesAgent
from exportdata.custom_makers.avitopayxml import AvitoXMLPay
from estatebase.models import Estate, EstateParam

    
class GdeetotdomXML(AvitoXML):
    name = 'gdeetotdom'
    def get_sales_agent(self, estate):
        return GdeetotdomSalesAgent(estate)
    def get_queryset(self):
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),             
             'agency_price__gte': MIN_PRICE_LIMIT,             
             }
        q = Estate.objects.all()
        q = q.filter(**f)      
        q = q.exclude(estate_params__exact = EstateParam.RENT,)     
        return q


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