from exportdata.custom_makers.avitoxml import AvitoXML, AvitoWrapper
from estatebase.models import Estate, EstateTypeCategory, EstateParam
from exportdata.xml_makers import SalesAgent
from lxml import etree


class NndvWrapper(AvitoWrapper):
    category_mapper =  {
                        EstateTypeCategory.KVARTIRAU4ASTOK:u'Дома, дачи, коттеджи', EstateTypeCategory.KVARTIRA:u'flat',
                        EstateTypeCategory.DOM:u'Дома, дачи, коттеджи', EstateTypeCategory.U4ASTOK: u'Земельные участки',
                        EstateTypeCategory.COMMERCE: u'Коммерческая недвижимость',
                        }

class NndvXML(AvitoXML):
    name = 'nndvxml'
    
    def __init__(self, nndv_wrapper):
        super(NndvXML,self).__init__(nndv_wrapper)
    
    def get_queryset(self):
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,
             'history__modificated__gte':self.get_delta(),             
             'agency_price__gte': MIN_PRICE_LIMIT,             
             }
        q = Estate.objects.all()
        q = q.filter(**f)        
        q = q.exclude(street__name__exact = u'без улицы')   
        q = q.exclude(estate_params__exact = EstateParam.RENT,)     
        return q
    
    def create_offer(self, estate):                
        self._wrapper.set_estate(estate)
        sa = SalesAgent(estate)
        offer = etree.Element("Ad")
        etree.SubElement(offer, "Id").text = str(estate.id)
        category = self._wrapper.estate_category() 
        etree.SubElement(offer, "Category").text = category
        etree.SubElement(offer, "OperationType").text = self._wrapper.offer_type()
        if self._wrapper.sale_rooms():
            etree.SubElement(offer, "SaleRooms").text = self._wrapper.sale_rooms()
        if self._wrapper.rooms():
            etree.SubElement(offer, "Rooms").text = self._wrapper.rooms()
        if category == u'Комнаты':             
            if self._wrapper.living_space():
                etree.SubElement(offer, "Square").text = self._wrapper.living_space()
        else:
            if self._wrapper.area():
                etree.SubElement(offer, "Square").text = self._wrapper.area()
        
        if self._wrapper.lot_area():
            etree.SubElement(offer, "LandArea").text = self._wrapper.lot_area()
            
        if self._wrapper.distance_to_city() is not None:
            etree.SubElement(offer, "DistanceToCity").text = self._wrapper.distance_to_city()
        
        if estate.estate_category_id != EstateTypeCategory.COMMERCE:                
            if self._wrapper.floor():            
                etree.SubElement(offer, "Floor").text = self._wrapper.floor()        
            if self._wrapper.floors_total():
                etree.SubElement(offer, "Floors").text = self._wrapper.floors_total()            
            if self._wrapper.house_type():
                etree.SubElement(offer, "HouseType").text = self._wrapper.house_type()            
            if self._wrapper.walls_type():
                etree.SubElement(offer, "WallsType").text = self._wrapper.walls_type()

        if estate.estate_category_id == EstateTypeCategory.KVARTIRA:
            etree.SubElement(offer, "MarketType").text = self._wrapper.new_flat()
                
        etree.SubElement(offer, "Region").text = self._wrapper.region()
        feed_locality = self._wrapper.feed_locality(self.name)
        etree.SubElement(offer, "City").text = feed_locality['city']
        if 'locality' in feed_locality:
            etree.SubElement(offer, "Locality").text = feed_locality['locality']
        
        etree.SubElement(offer, "District").text = self._wrapper.district()                            
        etree.SubElement(offer, "Street").text = self._wrapper.street()
        
        etree.SubElement(offer, "ObjectType").text = self._wrapper.object_type()
        
        
        etree.SubElement(offer, "Description").text = self._wrapper.description()
        etree.SubElement(offer, "Price").text = self._wrapper.price.value()
        images = self._wrapper.images(True)
        if images:
            images_root = etree.SubElement(offer, "Images")        
            if images:
                for image in images:
                    image_node = etree.SubElement(images_root, "Image")
                    image_node.set("url", image)
        etree.SubElement(offer, "CompanyName").text = sa.organization()
        etree.SubElement(offer, "EMail").text = sa.email()
        etree.SubElement(offer, "ContactPhone").text = sa.phones()[0]
        etree.SubElement(offer, "AdStatus").text = self._wrapper.ad_status()
        return offer 