# -*- coding: utf-8 -*-
from estatebase.helpers.functions import parse_decimal, split_digit
from estatebase.models import EstateParam, Document, Bidg, Stead, Estate
from migrate_app.models import TypesEstateType
class OrderPropMap(object):
    params = ('description', 'land_description', 
               'wall_material', 'real_estate_id', 
              'land_area_from', 'land_area_to', 
              'living_area_from', 'living_area_to'
               'total_area_from', 'total_area_to', 
               'year_built_from', 'year_built_to', )
    
    def __init__(self, bid):
        self.estate = bid
        self.pickle_dict = {}
    
    def get_setter(self, param):
        template = 'set_%s'
        return getattr(self, template % param, None)
    
    def set_param(self, param):
        if param not in self.params:
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
            if self.bid.note:                
                self.bid.note = self.bid.note + ', ' +  value
            else:
                self.bid.note = value
    
    def set_real_estate_id(self, value):
        if value:
            ids = split_digit(value)
            real_ids = Estate.objects.filter(id__in=ids).values_list('id', flat=True)
            if len(real_ids) > 0:
                self.pickle_dict['estates'] = real_ids
    
    def _set_types(self, types):
        result = []
        for t in types:
            estate_type = TypesEstateType.objects.get(source_id=t.type_id).estate_type
            if estate_type:
                result.append(estate_type)
        if len(result):
            self.pickle_dict['estate_types'] = result
            
                
                
       
