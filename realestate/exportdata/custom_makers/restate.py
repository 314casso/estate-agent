from estatebase.models import Estate, EstateParam
from exportdata.custom_makers.yaxmlplus import YandexPlusXML
from exportdata.xml_makers import SalesAgent


class Restate(YandexPlusXML):
    name = 'restate'    
    def get_queryset(self):
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),             
             'agency_price__gte': MIN_PRICE_LIMIT,  
             'estate_params__exact': EstateParam.PAYEXPORT,          
             }
        q = Estate.objects.all()
        q = q.filter(**f)     
        return q    
    
    def get_sales_agent(self, estate):
        return RestateSalesAgent(estate)
    
class RestateSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-918-492-7528'    


class IrrXML(Restate):
    name = 'irr'
    def get_sales_agent(self, estate):
        return IrrSalesAgent(estate)
    

class IrrSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-989-760-6007'
    
    
class NersXML(Restate):
    name = 'ners'
    def get_sales_agent(self, estate):
        return NersSalesAgent(estate)


class NersSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-989-770-6040'


class GdeetotdomXML(Restate):
    name = 'gdeetotdom'
    def get_sales_agent(self, estate):
        return GdeetotdomSalesAgent(estate)


class GdeetotdomSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-988-669-3067'
    

class CianYaXML(Restate):
    name = 'cianya'
    def get_sales_agent(self, estate):
        return CianYaSalesAgent(estate)


class CianYaSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-918-492-7529'    