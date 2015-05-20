from exportdata.custom_makers.avitoxml import AvitoXML
from estatebase.models import Estate, EstateTypeCategory, EstateParam

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