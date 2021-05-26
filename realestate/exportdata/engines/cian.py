# -*- coding: utf-8 -*-
import re
from exportdata.engines.base import BaseEngine
from lxml import etree
from exportdata.mappers.base import YandexMapper
import pytz
import datetime
from estatebase.models import EstateType, EstateTypeCategory, WallConstrucion


class CianEngine(BaseEngine):
    VERSION = '2' 
    def get_XHTML(self, lots, use_cache):
        self._use_cache = use_cache     
        xhtml = etree.Element('feed')        
        el_maker = self.el_maker(xhtml, [])
        el_maker("feed_version", self.VERSION)
        self.add_offers(xhtml, lots)
        return xhtml
    
    def square(self, el_maker, value, required=True, unit=u'кв. м'):
        el_maker("value", value, required)
        el_maker("unit", unit, required)               
    
    def create_offer(self, lot):                 
        mapper = CianMapper(lot, self._feed)
        empty_nodes = []          
        errors = {}
        warnings = {}    
        offer = etree.Element("object")
        el_maker = self.el_maker(offer, empty_nodes)
        el_maker("Category", mapper.category)
        el_maker("ExternalId", mapper.id)
        el_maker("Description", mapper.description)
        
        address = mapper.address 
        address_parts = []
        for field in ['region', 'locality', 'district', 'street']:
            value = getattr(address, field)
            if value and not value in address_parts:
                address_parts.append(value)                                         
        el_maker("Address", u', '.join(address_parts))     
               
        if mapper.coordinates and len(mapper.coordinates) == 2:
            el_coordinates = self.el_maker(etree.SubElement(offer, 'Coordinates'), empty_nodes)
            el_coordinates("Lat", str(mapper.coordinates[0]))               
            el_coordinates("Lng", str(mapper.coordinates[1]))
        
        
        contact = mapper.contact
        phones = etree.SubElement(offer, 'Phones')                
        el_phone_schema = self.el_maker(etree.SubElement(phones, 'PhoneSchema'), empty_nodes)        
        el_phone_schema("CountryCode", "+7")               
        el_phone_schema("Number", mapper.phone_cleaner(contact.phone))
        
        max_images = 20 
               
        images = mapper.images(max_images)
        if images:
            photos = etree.SubElement(offer, 'Photos')                    
            for image in images:
                el_photos_schema = self.el_maker(etree.SubElement(photos, 'PhotoSchema'), empty_nodes)                
                el_photos_schema("FullUrl", image)               
                
        
        if mapper.category in [u'flatShareSale', u'flatSale']:
            el_maker("FlatRoomsCount", mapper.rooms)            
            el_maker("IsApartments", mapper.apartments, False)
         
        
        if mapper.category not in [u'landSale']:
            area = mapper.living_space if mapper.category in [u'flatShareSale'] else mapper.area            
            el_maker("TotalArea", area)
            el_maker("FloorNumber", mapper.floor, False)    
        
            if mapper.new_flat:            
                el_jk_schema = self.el_maker(etree.SubElement(offer, 'JKSchema'), empty_nodes)
                el_jk_schema('Id', mapper.jk_schema_id)
                el_jk_schema('Name', mapper.building_name)
            
            
            if mapper.rooms_space is not None:
                if len(mapper.rooms_space) != mapper.get_rooms():
                    warnings['rooms_space'] = u'Количество комнат %s, с указанной площадью %s' % (mapper.rooms, len(mapper.rooms_space))
                else:
                    room_definitions = etree.SubElement(offer, 'RoomDefinitions')
                    for room_space in mapper.rooms_space:
                        el_room = self.el_maker(etree.SubElement(room_definitions, 'Room'), empty_nodes)
                        el_room("Area", room_space)                    
            
            if mapper.living_space:             
                el_maker('LivingArea', mapper.living_space, False)
            if mapper.kitchen_space:                   
                el_maker('KitchenArea', mapper.kitchen_space, False)        
            
            if mapper.balcons_count:
                el_maker('BalconiesCount', str(mapper.balcons_count), False)            
            
            el_building = self.el_maker(etree.SubElement(offer, 'Building'), empty_nodes)
            el_building('FloorsCount', mapper.floors)
            el_building('BuildYear', mapper.built_year, False)
            el_building('MaterialType', mapper.material_type, False)
            el_building('CeilingHeight', mapper.ceiling_height, False)
            el_building('PassengerLiftsCount', mapper.ceiling_height, False)
            #TODO         HeatingType
        
        price = mapper.price
        el_bargain_terms = self.el_maker(etree.SubElement(offer, 'BargainTerms'), empty_nodes)
        el_bargain_terms('Price', price.value)
        el_bargain_terms('Currency', price.currency)
        el_bargain_terms('MortgageAllowed', mapper.mortgage, False)
        el_bargain_terms('SaleType', mapper.sale_type, False)
        
                
        if mapper.category not in [u'flatSale', u'roomSale', u'flatShareSale', u'newBuildingFlatSale']:            
            el_maker("HasWater", mapper.water_supply, False)
            el_maker("HasDrainage", mapper.sewerage_supply, False)            
            el_maker("HasElectricity", mapper.electricity_supply, False)
            el_maker("HasGas", mapper.gas_supply, False)
            
            el_land = self.el_maker(etree.SubElement(offer, 'Land'), empty_nodes)
            el_land('Area', mapper.land_area)
            el_land('AreaUnitType', u'sotka')
            #TODO         Status
        
        
        if mapper.category in [u'houseShareSale']:
            el_maker("ShareAmount", "50%")    
            
        if len(empty_nodes):
            errors['empty_nodes'] = u', '.join(empty_nodes)
            
        return (offer, {'errors': errors, 'warnings': warnings})

class CianMapper(YandexMapper):
    _coordinates = None   
    _jk_schema_id = None
    _balcons_count = None 
    _material_type = None
    
    @property        
    def balcons_count(self):
        if not self._balcons_count and self._basic_bidg:             
            self._balcons_count = self._basic_bidg.get_balcons_count()                
        return self._balcons_count         
    
    def bool_to_xml(self, bool_value):
        return u'true' if bool_value else u'false'
    
    def get_category(self):                                                                         
        category = self.get_value_mapper(EstateType, self._estate_type_id, 'ObjectType')
        if category:
            return category             
        return self.get_value_mapper(EstateTypeCategory, self._estate.estate_category_id, 'Category')
    
    @property
    def coordinates(self):
        if not self._coordinates:
            if self._estate.latitude and self._estate.longitude: 
                self._coordinates = (self._estate.latitude, self._estate.longitude)                
        return self._coordinates
      
    @property
    def material_type(self):
        if not self._material_type:
            if self._basic_bidg:                
                self._material_type = self.get_value_mapper(WallConstrucion, self._basic_bidg.wall_construcion_id, 'WallsType')
        return self._material_type  
        
    @property
    def jk_schema_id(self):
        if not self._jk_schema_id:
            if self.new_flat:
                yandex_building = self.get_yandex_building()
                if yandex_building:
                    self._jk_schema_id = u'%s' % yandex_building.cian_complex_id
        return self._jk_schema_id
    
    def phone_cleaner(self, phone):
        pattern = r"^(\+7|8)[\-\s]*"
        return re.sub(pattern, '', phone)
    
    @property
    def sale_type(self):
        return u'free'    
    
    class Price(YandexMapper.Price):      
        @property    
        def currency(self):
            return u'rur'  
        
