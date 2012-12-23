# -*- coding: utf-8 -*-
from estatebase.helpers.functions import parse_decimal, split_digit
from estatebase.models import EstateParam, Document, Bidg, Stead
class PropMap(object):
    params = ('all_floor', 'description', 'electricity_status', 'gas_status', 'land_description', 
              'sewerage_status', 'state', 'wall_material', 'water_status', 'real_estate_id', 
              'destination', 'distance_from', 'distance_to', 'electricity_distance', 'floor_from', 
              'floor_to', 'gas_distance', 'internet_status', 'land_area_from', 'land_area_to', 
              'land_front', 'living_area_from', 'living_area_to', 'phone_status', 'porch_distance', 
              'porch_status', 'rooms_from', 'rooms_to', 'sewerage_distance', 'total_area_from', 
              'total_area_to', 'water_distance', 'year_built_from', 'year_built_to', 'mortgage', 
              'floor_not_end', 'facing', 'evidence', 'exchange', 'elevator', 'land_evidence')
    
#Кол заявки, Дата создания, создатель, Коды, тип объекта, район, населенные пункты, цена, 
#дополнительное описание к внешнему описанию и участку в одно поле в новой базе.
#Остальные поля, если не затратно по времени и силам: 
#общ площадь, колво комнат, материал стен, площадь участка, год постройки Но не обязательно! 

    
    def __init__(self, bid):
        self.estate = bid
        self.pickle_dict = {}
    
    def get_setter(self, param):
        template = 'set_%s'
        return getattr(self, template % param, None)
    
    def set_param(self, param):
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
            if len(ids) > 0:
                self.bid.estates = ids   
