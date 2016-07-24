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
        
        el_maker("Street", u', '.join(street), False)
        if mapper.category in [u'Дома, дачи, коттеджи', u'Земельные участки']:
            el_maker("DistanceToCity", address.distance_to_city, mapper.category in [u'Дома, дачи, коттеджи', u'Земельные участки'])
        el_maker("Description", mapper.description)
        el_maker("Rooms", mapper.rooms,  
                 required=(mapper.category in [u'Квартиры', u'Комнаты'])
                       )
        
        if mapper.category in [u'Коммерческая недвижимость']:
            el_maker("Title", mapper.title, False)
            
        etree.SubElement(offer, "Price").text = mapper.price.value()
        etree.SubElement(offer, "PriceType").text = mapper.price.type()
        square = mapper.living_space if mapper.category in [u'Комнаты'] else mapper.area         
        el_maker("Square", square, required=(mapper.category not in [u'Земельные участки']))
        el_maker("LandArea", mapper.land_area, required=(mapper.category in [u'Земельные участки', u'Дома, дачи, коттеджи']))
        
        if mapper.category in [u'Квартиры', u'Комнаты']:
            el_maker("Floor", mapper.floor)        
        
        el_maker("Floors", mapper.floors, required=(mapper.category in [u'Квартиры', u'Комнаты', u'Дома, дачи, коттеджи']))
        
        if mapper.category in [u'Квартиры', u'Комнаты']:
            el_maker("HouseType", mapper.house_type)
            
        if mapper.category in [u'Дома, дачи, коттеджи']:
            el_maker("WallsType", mapper.walls_type)
            
        if mapper.category in [u'Квартиры']:
            el_maker("MarketType", mapper.market_type)
            
        if mapper.category not in [u'Квартиры', u'Комнаты']:
            el_maker("ObjectType", mapper.object_type)        
             
        images = mapper.images(10)
        print images
        if images:
            images_root = etree.SubElement(offer, "Images")       
            for image in images:
                etree.SubElement(images_root, "Image", {'url': image})                
        
        if len(empty_nodes):
            errors['empty_nodes'] = u', '.join(empty_nodes)
                   
        return (offer, errors)  
