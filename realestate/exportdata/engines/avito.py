# -*- coding: utf-8 -*-
from exportdata.engines.base import BaseEngine
from lxml import etree
from exportdata.mappers.base import AvitoMapper


class AvitoEngine(BaseEngine):   
    feed_locality_name = 'avito'
    root = 'Ads'     
    target = 'Avito.ru'         
    version = '3'    
            
    def get_XHTML(self, lots, use_cache):
        self._use_cache = use_cache     
        xhtml = etree.Element(self.root)
        xhtml.set("target", self.target)
        xhtml.set("formatVersion", self.version)
        self.add_offers(xhtml, lots)
        return xhtml
            
    def create_offer(self, lot):        
        mapper = AvitoMapper(lot, self._feed)
        empty_nodes = []  
        errors = {}     
        offer = etree.Element("Ad")
        el_maker = self.el_maker(offer, empty_nodes)
        el_maker("Id", mapper.id)        
        el_maker("Category", mapper.category)
        el_maker("AdStatus", mapper.ad_status)
        el_maker("OperationType", mapper.operation_type)        
        el_maker("AllowEmail", mapper.allow_email)        
        
        contact = mapper.contact                
        el_maker("ManagerName", contact.manager_name)
        el_maker("ContactPhone", contact.phone)
                
        address = mapper.address
        el_maker("Region", address.region)                      
        el_maker("City", address.city, False)
        street = []
        if not address.city:
            street.append(address.district)
            street.append(address.locality)
        if mapper.category in [u'Квартиры', u'Комнаты', u'Дома, дачи, коттеджи', u'Коммерческая недвижимость'] and not address.street:
            empty_nodes.append("Street")
        street.append(address.street)    
        if mapper.category in [u'Квартиры', u'Комнаты']:
            if address.bld_number:
                street.append(address.bld_number)
            else:
                empty_nodes.append("BldNumber")               
         
        el_maker("Street", u', '.join(street), True)
                    
        el_maker("Rooms", mapper.rooms,  
                 required=(mapper.category in [u'Квартиры', u'Комнаты'])
                 )

#         if category == u'Комнаты':             
#             if self._wrapper.living_space():
#                 etree.SubElement(offer, "Square").text = self._wrapper.living_space()
#         else:
#             if self._wrapper.area():
#                 etree.SubElement(offer, "Square").text = self._wrapper.area()
#         
#         if self._wrapper.lot_area():
#             etree.SubElement(offer, "LandArea").text = self._wrapper.lot_area()
#             
#         if self._wrapper.distance_to_city() is not None:
#             etree.SubElement(offer, "DistanceToCity").text = self._wrapper.distance_to_city()
#         
#         if estate.estate_category_id != EstateTypeCategory.COMMERCE:                
#             if self._wrapper.floor():            
#                 etree.SubElement(offer, "Floor").text = self._wrapper.floor()        
#             if self._wrapper.floors_total():
#                 etree.SubElement(offer, "Floors").text = self._wrapper.floors_total()            
#             if self._wrapper.house_type():
#                 etree.SubElement(offer, "HouseType").text = self._wrapper.house_type()            
#             if self._wrapper.walls_type():
#                 etree.SubElement(offer, "WallsType").text = self._wrapper.walls_type()
# 
#         if estate.estate_category_id == EstateTypeCategory.KVARTIRA:
#             etree.SubElement(offer, "MarketType").text = self._wrapper.new_flat()
#                 
#         etree.SubElement(offer, "Region").text = self._wrapper.region()
#         feed_locality = self._wrapper.feed_locality(self.feed_locality_name)
#         etree.SubElement(offer, "City").text = feed_locality['city']
#         if 'locality' in feed_locality:
#             etree.SubElement(offer, "Locality").text = feed_locality['locality']
#         
#         etree.SubElement(offer, "District").text = self._wrapper.district()                            
#         etree.SubElement(offer, "Street").text = self._wrapper.street()
#         
#         etree.SubElement(offer, "ObjectType").text = mapper.object_type()
#         
#         
#         etree.SubElement(offer, "Description").text = self._wrapper.description()
        etree.SubElement(offer, "Price").text = mapper.price.value()
        etree.SubElement(offer, "PriceType").text = mapper.price.type()
        
#         images = self._wrapper.images(True)
#         if images:
#             images_root = etree.SubElement(offer, "Images")        
#             if images:
#                 for image in images:
#                     image_node = etree.SubElement(images_root, "Image")
#                     image_node.set("url", image)
#         etree.SubElement(offer, "CompanyName").text = sa.organization()
#         etree.SubElement(offer, "EMail").text = sa.email()
#         etree.SubElement(offer, "ContactPhone").text = sa.head_phone()
        
        if len(empty_nodes):
            errors['empty_nodes'] = u', '.join(empty_nodes)
                   
        return (offer, errors) 
    
