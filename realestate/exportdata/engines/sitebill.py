# -*- coding: utf-8 -*-
from exportdata.mappers.base import YandexMapper
from lxml import etree
from exportdata.engines.base import BaseEngine
import datetime
import pytz


class Sitebill(BaseEngine):
    def get_XHTML(self, lots, use_cache):
        self._use_cache = use_cache    
        xhtml_namespace = "http://webmaster.yandex.ru/schemas/feed/realty/2010-06"    
        XHTML = "{%s}%s" % (xhtml_namespace, 'realty-feed')
        NSMAP = {None : xhtml_namespace}              
        xhtml = etree.Element(XHTML, nsmap=NSMAP)
        tz = pytz.timezone('Europe/Moscow')
        etree.SubElement(xhtml, "generation-date").text = tz.localize(datetime.datetime.now()).replace(microsecond=0).isoformat()            
        self.add_offers(xhtml, lots)
        return xhtml
    
    def square(self, el_maker, value, required=True, unit=u'кв. м'):
        el_maker("value", value, required)
        el_maker("unit", unit, required) 
    
    def create_offer(self, lot):                 
        mapper = SitebillMapper(lot, self._feed)
        empty_nodes = []          
        errors = {}
        warnings = {}    
        offer = etree.Element("offer", {'internal-id':mapper.id})
        el_maker = self.el_maker(offer, empty_nodes)
        el_maker("type", mapper.type)
        el_maker("category", mapper.category)
        if mapper.category not in [u'Коммерческая недвижимость']:
            el_maker("property-type", mapper.property_type)        
        if mapper.category in [u'Коммерческая недвижимость']:
            el_maker("commercial-type", mapper.object_type)
            
        el_maker("url", mapper.url)    
        el_maker("creation-date", mapper.creation_date)
        el_maker("last-update-date", mapper.last_update_date)
        
        address = mapper.address                  
        el_location = self.el_maker(etree.SubElement(offer, 'location'), empty_nodes)
        el_location("country", address.country)
        el_location("region", address.region)
        el_location("district", address.district)
        el_location("locality-name", address.locality_with_type)
        el_location("sub-locality-name", address.sub_locality, False)
        el_location("address", address.street, not mapper.suburban if mapper._feed.use_possible_street else False)
        
        contact = mapper.contact  
        sales_agent = etree.SubElement(offer, 'sales-agent') 
        el_sales_agent = self.el_maker(sales_agent, empty_nodes)              
        el_sales_agent("name", contact.manager_name)
        el_sales_agent("phone", contact.phone)       
        el_sales_agent("category", contact.category)
        el_sales_agent("organization", contact.organization)
        el_sales_agent("url", contact.url)
        el_sales_agent("email", contact.email)
        
        price = mapper.price                
        el_price = self.el_maker(etree.SubElement(offer, 'price'), empty_nodes)           
        el_price("value", price.value, False)
        el_price("currency", price.currency, False)
        
        el_maker("mortgage", mapper.mortgage, False)
                
        if mapper.category not in [u'Земельные участки']:
            area = mapper.living_space if mapper.category in [u'Комнаты'] else mapper.area
            self.square(self.el_maker(etree.SubElement(offer, 'area'), empty_nodes), area)
        
        if mapper.category in [u'Земельные участки', u'Дома', u'Дома']:
            self.square(self.el_maker(etree.SubElement(offer, 'lot-area'), empty_nodes), mapper.land_area, True, u'сот')
            
        if mapper.rooms_space is not None:
            if len(mapper.rooms_space) != mapper.get_rooms():
                warnings['rooms_space'] = u'Количество комнат %s, с указанной площадью %s' % (mapper.rooms, len(mapper.rooms_space))
            else:
                for room_space in mapper.rooms_space:
                    self.square(self.el_maker(etree.SubElement(offer, 'room-space'), empty_nodes), room_space)
        
        if mapper.living_space:             
            self.square(self.el_maker(etree.SubElement(offer, 'living-space'), empty_nodes), mapper.living_space, False)
        if mapper.kitchen_space:                   
            self.square(self.el_maker(etree.SubElement(offer, 'kitchen-space'), empty_nodes), mapper.kitchen_space, False)
        
        el_maker("renovation", mapper.renovation, False)
        el_maker("quality", mapper.quality, False)
        
        el_maker("description", mapper.description)
        
        if mapper.category in [u'Земельные участки']:
            el_maker("lot-type", mapper.lot_type)
            
        if mapper.new_flat:
            el_maker("new-flat", mapper.new_flat)    
            
        if mapper.category in [u'Дома', u'Квартиры']:
            el_maker("rooms", mapper.rooms)    
            
        if mapper.category in [u'Комнаты']:
            el_maker("rooms-offered", mapper.rooms)
        
        if mapper.category in [u'Квартиры']:
            el_maker("studio", mapper.studio, False)
            el_maker("apartments", mapper.apartments, False)
            
        if mapper.category in [u'Квартиры', u'Комнаты']:
            el_maker("floor", mapper.floor)
            
        if mapper.category in [u'Квартиры', u'Комнаты']:
            el_maker("rooms-type", mapper.rooms_type, False)
        
        el_maker("internet", mapper.internet, False)
        el_maker("room-furniture", mapper.room_furniture, False)
        el_maker("floor-covering", mapper.floor_covering, False)
        el_maker("window-view", mapper.window_view, False)
        
        if mapper.category not in [u'Коммерческая недвижимость']:    
            el_maker("phone", mapper.phone, False)  
            el_maker("kitchen-furniture", mapper.kitchen_furniture, False)            
            el_maker("television", mapper.television, False)
            el_maker("balcony", mapper.balcony, False)
            el_maker("bathroom-unit", mapper.bathroom_unit, False)            
        
        if mapper.category in [u'Коммерческая недвижимость']:
            el_maker("rooms", mapper.rooms, False)
            el_maker("floor", mapper.floor, False)
            el_maker("air-conditioner", mapper.air_conditioner, False)
            el_maker("ventilation", mapper.ventilation, False)
        
        if mapper.category in [u'Коммерческая недвижимость', u'Дома']:
            el_maker("heating-supply", mapper.heating_supply, False)
            el_maker("water-supply", mapper.water_supply, False)
            el_maker("sewerage-supply", mapper.sewerage_supply, False)            
            el_maker("electricity-supply", mapper.electricity_supply, False)
            el_maker("gas-supply", mapper.gas_supply, False)
        
        el_maker("floors-total", mapper.floors, mapper.new_flat)
       
        el_maker("building-type", mapper.building_type, False)
        el_maker("built-year", mapper.built_year, mapper.new_flat)
        
        if mapper.new_flat:
            el_maker("building-name", mapper.building_name, mapper.new_flat)
            el_maker("ready-quarter", mapper.ready_quarter)
            el_maker("building-state", mapper.building_state)
            el_maker("yandex-building-id", mapper.yandex_building_id, mapper.new_flat)
        
        el_maker("lift", mapper.lift, False)
        el_maker("ceiling-height", mapper.ceiling_height, False)
        
        el_maker("deal-status", mapper.deal_status)
                     
        max_images = {     
            u'Квартиры' : 20,
            u'Комнаты' : 10,
            u'Дома' : 20,
            u'Земельные участки' : 5,            
            u'Коммерческая недвижимость' : 10           
        }
               
        images = mapper.images(max_images.get(mapper.category, 5))
        if images:        
            for image in images:
                el_maker("image", image)    
                           
        
        if len(empty_nodes):
            errors['empty_nodes'] = u', '.join(empty_nodes)
                   
        return (offer, {'errors': errors, 'warnings': warnings})
        

class SitebillMapper(YandexMapper):    
    class Address(YandexMapper.Address):
        _locality_type = None           
        _locality_with_type = None
        
        @property
        def locality_type(self):
            if not self._locality_type:
                if self._estate.locality and self._estate.locality.locality_type:
                    self._locality_type = u"%s" % self._estate.locality.locality_type.name
                    self._locality_type = self._locality_type.lower()                    
            return self._locality_type
        
        @property
        def locality_with_type(self):
            if not self._locality_with_type:
                self._locality_with_type = u"%s %s" % (self.locality_type, self.locality)
            return self._locality_with_type
            
        
        
    