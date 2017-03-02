# -*- coding: utf-8 -*-
from exportdata.engines.base import BaseEngine
from lxml import etree
from exportdata.mappers.base import AvitoMapper


class AvitoEngine(BaseEngine): 
    VERSION = '3' 
    def get_XHTML(self, lots, use_cache):
        self._use_cache = use_cache     
        xhtml = etree.Element('Ads')
        xhtml.set("target", 'Avito.ru')
        xhtml.set("formatVersion", self.VERSION)
        self.add_offers(xhtml, lots)
        return xhtml
            
    def create_offer(self, lot):                 
        mapper = AvitoMapper(lot, self._feed)
        empty_nodes = []  
        errors = {}  
        warnings = {}   
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
        
        street = []        
        if address.city:
            el_maker("City", address.city, False)        
        else:
            el_maker("City", address.metropolis, False)
            street.append(address.district)
            street.append(address.locality)
        if mapper._feed.use_possible_street and mapper.category in [u'Квартиры', u'Комнаты', u'Дома, дачи, коттеджи', u'Коммерческая недвижимость'] and not address.street:
            empty_nodes.append("Street")
        if address.street:
            street.append(address.street)    
        
        if mapper._feed.use_possible_street and mapper._feed.show_bld_number:
            if mapper.category in [u'Квартиры', u'Комнаты']:
                if address.bld_number:
                    street.append(address.bld_number)
                else:
                    empty_nodes.append("BldNumber")               
        
        el_maker("Street", u', '.join([s for s in street if s is not None]), False)
        if mapper.category in [u'Дома, дачи, коттеджи', u'Земельные участки']:
            el_maker("DistanceToCity", address.distance_to_city, mapper.category in [u'Дома, дачи, коттеджи', u'Земельные участки'])
        el_maker("Description", mapper.description)
        
        if mapper.category in [u'Квартиры', u'Комнаты']:
            el_maker("Rooms", mapper.rooms)
        
        price = mapper.price        
        if mapper.category in [u'Коммерческая недвижимость']:
            el_maker("Title", mapper.title, False)
            el_maker("PriceType", price.type, False)
                    
        el_maker("Price", price.value, False)
        
        square = mapper.living_space if mapper.category in [u'Комнаты'] else mapper.area                 
        el_maker("Square", square, required=(mapper.category not in [u'Земельные участки']))
        
        if mapper.category in [u'Земельные участки', u'Дома, дачи, коттеджи']:
            el_maker("LandArea", mapper.land_area)
        
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
        
        if mapper.living_space:             
            el_maker("LivingSpace", mapper.living_space, False)
            
        if mapper.kitchen_space:
            el_maker("KitchenSpace", mapper.kitchen_space, False)
             
        max_images = {     
            u"Квартиры" : 20,
            u"Комнаты" : 10,
            u"Дома, дачи, коттеджи" : 20,
            u"Земельные участки" : 5,
            u"Гаражи и машиноместа" : 5,
            u"Коммерческая недвижимость" : 10,
            u"Недвижимость за рубежом" : 10
        }
             
        images = mapper.images(max_images.get(mapper.category, 5))        
        if images:
            images_root = etree.SubElement(offer, "Images")       
            for image in images:
                etree.SubElement(images_root, "Image", {'url': image})                
        
        if len(empty_nodes):
            errors['empty_nodes'] = u', '.join(empty_nodes)
                   
        return (offer, {'errors': errors, 'warnings': warnings})  
