from estatebase.models import Estate, EstateParam
from exportdata.custom_makers.yaxmlplus import YandexPlusXML


class Restate(YandexPlusXML):
    name = 'restate'
    
    def get_queryset(self):
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,
#              'history__modificated__gte':self.get_delta(),             
             'agency_price__gte': MIN_PRICE_LIMIT,  
#              'street__isnull': False, 
             'estate_params__exact': EstateParam.PAYEXPORT,          
             }
        q = Estate.objects.all()
        q = q.filter(**f)     
        return q    