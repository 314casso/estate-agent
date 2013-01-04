# -*- coding: utf-8 -*-
from estatebase.helpers.functions import parse_decimal, split_digit
from estatebase.models import EstateParam, Document, Bidg, Stead, Estate
from migrate_app.models import TypesEstateType
from migrate_app.prop_map import get_wall_map, get_state_map
class OrderPropMap(object):
    params = ('description', 'land_description', 
               'wall_material', 'real_estate_id', 
              'land_area_from', 'land_area_to', 
              'living_area_from', 'living_area_to'
               'total_area_from', 'total_area_to', 
               'year_built_from', 'year_built_to', 
               'rooms_from', 'rooms_to',
               'state'
               )
    
    def __init__(self, bid):        
        self.pickle_dict = {}
        self.bid = bid
    
    def get_setter(self, param):
        template = 'set_%s'
        return getattr(self, template % param, None)
    
    def set_param(self, param):        
        if param.name not in self.params:
            return
        value = param.value.strip()
        if not value or value == '0':
            return         
        #print 'Call setter %s' % param.name
        param_setter = self.get_setter(param.name)  
        if not param_setter:
            if param.name not in []:
                print u'Setter for %s not found!' % param.name
                pass
        else:
            try:
                param_setter(param.value)
            except AttributeError:
                print u'%s' % (param.name)
               
    def set_description(self, value):        
        if value:
            if self.bid.note:                
                self.bid.note = self.bid.note + ', ' +  value
            else:
                self.bid.note = value
    
    def set_land_description(self, value):        
        if value:
            value = u'участок: %s' % value 
            if self.bid.note:                
                self.bid.note = self.bid.note + ', ' +  value
            else:
                self.bid.note = value
    
    def set_real_estate_id(self, value):
        if value:
            ids = split_digit(value)
            real_ids = list(Estate.objects.filter(id__in=ids).all())
            if len(real_ids) > 0:
                self.pickle_dict['estates'] = real_ids
    
    def _set_types(self, types):
        result = []
        for t in types:
            estate_type = TypesEstateType.objects.get(source_id=t).estate_type
            if estate_type:
                result.append(estate_type)
        if len(result):
            self.pickle_dict['estate_type'] = result
    
              
    def _values_to_pickle(self, value, key, p_map):               
        values = value.split(',')                
        for value in values:     
            m_val = p_map[value.strip()]       
            if key in self.pickle_dict and len(self.pickle_dict[key]):
                self.pickle_dict[key].append(m_val)
            else:
                self.pickle_dict[key] = [m_val,]
    
    def set_wall_material(self, value):
        self._values_to_pickle(value, 'wall_construcion', get_wall_map())
    
    def _two_values_helper(self, key, value, index):
        if value:
            if not key in self.pickle_dict:
                self.pickle_dict[key]=[None,None]               
            self.pickle_dict[key][index] = value                            
    
    def set_land_area_from(self, value):        
        self._two_values_helper('stead_area',value, 0)
    
    def set_land_area_to(self, value):        
        self._two_values_helper('stead_area',value, 1)
        
    def set_living_area_from(self, value):        
        self._two_values_helper('used_area',value, 0)
    
    def set_living_area_to(self, value):        
        self._two_values_helper('used_area',value, 1)
    
    def set_total_area_from(self, value):        
        self._two_values_helper('total_area',value, 0)
    
    def set_total_area_to(self, value):        
        self._two_values_helper('total_area',value, 1)
    
    def set_year_built_from(self, value):        
        self._two_values_helper('year_built',value, 0)
    
    def set_year_built_to(self, value):        
        self._two_values_helper('year_built',value, 1)
    
    def set_rooms_from(self, value):        
        self._two_values_helper('room_count',value, 0)    
    
    def set_rooms_to(self, value):        
        self._two_values_helper('room_count',value, 1)
    
    def set_state(self, value):
        self._values_to_pickle(value, 'interior', get_state_map()) 
         
      

