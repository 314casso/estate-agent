from estatebase.models import Estate, EstateParam
from exportdata.custom_makers.yaxmlplus import YandexPlusXML, YandexPlusWrapper


class YaPlusPhotoWrapper(YandexPlusWrapper):
    def district(self):
        if self._estate.region.id in (2,3):
            return None
        return self._estate.region.regular_name


class YaPlusPhoto(YandexPlusXML):
    name = 'yaplusphoto'
    
    def __init__(self, ya_plus_photo_wrapper):
        super(YandexPlusXML,self).__init__(ya_plus_photo_wrapper)
            
    def get_queryset(self):
        print self._wrapper        
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),             
             'agency_price__gte': MIN_PRICE_LIMIT,
             'street__isnull': False,     
             'images__isnull': False,                     
             }
        q = Estate.objects.all()
        q = q.filter(**f)    
        q = q.exclude(estate_params__exact=EstateParam.RENT,)                      
        return q.distinct('id')