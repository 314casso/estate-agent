from exportdata.custom_makers.avitoxml import AvitoXML
from estatebase.models import Estate, EstateTypeCategory, EstateParam
from exportdata.xml_makers import SalesAgent

class AvitoXMLPay(AvitoXML):
    name = 'avitopay'
    def get_queryset(self):        
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,                          
             'agency_price__gte': MIN_PRICE_LIMIT,
             'estate_category_id__in': (EstateTypeCategory.KVARTIRA, EstateTypeCategory.DOM, EstateTypeCategory.KVARTIRAU4ASTOK, 
                                        EstateTypeCategory.U4ASTOK, EstateTypeCategory.COMMERCE),             
             'estate_params__exact': EstateParam.AVITO,             
             }
        q = Estate.objects.all()
        q = q.filter(**f)
        return q
    
    def get_sales_agent(self, estate):
        return AvitoPaySalesAgent(estate)
    
class AvitoPaySalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-918-040-9494'