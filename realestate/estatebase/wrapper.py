# -*- coding: utf-8 -*-
from copy import deepcopy

APARTMENT = 0
NEWAPART = 1
HOUSE = 2 
STEAD = 3
OUTBUILDINGS = 4
AGRICULTURAL = 5
APARTMENTSTEAD = 6
FACILITIES = 7

class FieldWrapper():
    def __init__(self, name, label, value=None):
        self.name = name
        self.label = label    

class BaseWrapper(object):    
    _exterior_set = None    
    _interior_set = None
    _extra_set = None
    @property           
    def exterior_set(self):
        return self._exterior_set
    @exterior_set.setter
    def exterior_set(self, val):
        self._exterior_set = val      
    @property
    def extra_set(self):
        return self._extra_set    
    @extra_set.setter
    def extra_set(self, val):
        self._extra_set = val
    @property
    def interior_set(self):
        return self._interior_set
    @interior_set.setter
    def interior_set(self, val):
        self._interior_set = val
    @property        
    def full_set(self):
        result = []
        if self.exterior_set:         
            result.extend(self.exterior_set)
        if self.extra_set:     
            result.extend(self.extra_set)
        if self.interior_set:    
            result.extend(self.interior_set)        
        return result
    def get_label(self, field):
        return getattr(self, field, None)
                   
class BidgWrapper(BaseWrapper):
    summary_set = ['total_area', 'used_area', 'room_count', 'wall_construcion', 'exterior_finish', 'year_built', 'floor', 'floor_count']
    def __init__(self):                
        self.exterior_set = ['estate_type', 'room_number', 'year_built', 'floor', 'floor_count', 'elevator', 'wall_construcion', 'exterior_finish', 'window_type', 'roof', 'heating', 'ceiling_height', 'room_count', 'total_area', 'used_area']    
        self.interior_set = ['wall_finish', 'flooring', 'ceiling', 'interior', 'appliances']
        self.extra_set = ['documents']
    @property    
    def exterior_report_set(self):
        result = self.exterior_set[:]        
        exclude_set = ('estate_type','room_number')
        for f in exclude_set:
            try:             
                result.remove(f)
            except:
                pass               
        return result

class ApartmentWrapper(BidgWrapper):
    @BidgWrapper.exterior_set.getter
    def exterior_set(self):
        result = super(ApartmentWrapper, self).exterior_set[:]
        exclude_set = ('roof',)
        for f in exclude_set:
            try:             
                result.remove(f)
            except:
                pass               
        return result         
            
class NewapartWrapper(ApartmentWrapper):    
    year_built = u'Год сдачи'    

class HomeWrapper(BidgWrapper):
    @BidgWrapper.exterior_set.getter
    def exterior_set(self):
        result = super(HomeWrapper, self).exterior_set[:]
        exclude_set = ('room_number','floor', 'elevator')
        for f in exclude_set:
            try:             
                result.remove(f)
            except:
                pass               
        return result

class ApartmentSteadWrapper(BidgWrapper):
    '''
    Участок с квартирой
    '''
    @BidgWrapper.exterior_set.getter
    def exterior_set(self):
        result = super(BidgWrapper, self).exterior_set[:]
        exclude_set = ('elevator','room_number')
        for f in exclude_set:
            try:             
                result.remove(f)
            except:
                pass               
        return result

class OutbuildingsWrapper(BidgWrapper):
    def __init__(self):
        self.exterior_set = ['year_built', 'floor_count', 'wall_construcion', 'exterior_finish', 'room_count', 'total_area', 'description']
        self.interior_set = ['wall_finish', 'flooring', 'ceiling', 'interior', 'appliances']
        self.extra_set = []
    
class FacilitiesWrapper(BidgWrapper):
    def __init__(self):
        self.exterior_set = ['description']
        self.interior_set = []
        self.extra_set = []    
    
class SteadWrapper(BaseWrapper):
    #    land_type = u'Земля ТЕСТ'    
    def __init__(self):        
        self._field_set = ['total_area', 'face_area', 'shape', 'land_type' ]
        self.extra_set = ['documents']
        self.exterior_set = deepcopy(self._field_set)   
    @property
    def field_set(self):
        return self._field_set
    @property
    def field_report_set(self):
        return self.field_set
            
def get_polymorph_label(template, field):            
    wrapper = get_wrapper(template)    
    try:
        return getattr(wrapper, field)
    except AttributeError:
        return None

WRAPPERS = {
           APARTMENT:(ApartmentWrapper(), None),
           NEWAPART:(NewapartWrapper(), None),
           HOUSE:(HomeWrapper(), SteadWrapper()),
           STEAD:(None, SteadWrapper()),
           OUTBUILDINGS:(OutbuildingsWrapper(), None),
           AGRICULTURAL:(None, SteadWrapper()),
           APARTMENTSTEAD:(ApartmentSteadWrapper(), SteadWrapper()),
           FACILITIES:(FacilitiesWrapper(), None),
           }
   
def get_wrapper(obj):    
    if obj.estate_type.template is None:
        raise Exception(u'Не указан шаблон для вида недвижимости %s!' % obj.estate_type)
    if type(obj).__name__ == 'Bidg':
        return WRAPPERS[obj.estate_type.template][0]
    elif type(obj).__name__ == 'Stead':        
        return WRAPPERS[obj.estate_type.template][1]