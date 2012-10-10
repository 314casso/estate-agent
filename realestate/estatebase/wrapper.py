# -*- coding: utf-8 -*-

APARTMENT = 0
NEWAPART = 1
HOUSE = 2 
STEAD = 3
OUTBUILDINGS = 4

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
        result.extend(self.exterior_set)
        result.extend(self.extra_set)
        result.extend(self.interior_set)        
        return result    
    def get_label(self, field):
        return getattr(self, field, None)
                   
class BidgWrapper(BaseWrapper):
    def __init__(self):                
        self.exterior_set = ['estate_type', 'room_number', 'year_built', 'floor', 'floor_count', 'elevator', 'wall_construcion', 'exterior_finish', 'window_type', 'roof', 'heating', 'ceiling_height', 'room_count', 'total_area', 'used_area', 'wall_finish', 'flooring', 'ceiling', 'interior']    
        self.interior_set = ['wall_finish', 'flooring', 'ceiling', 'interior']
        self.extra_set = ['documents']      

class ApartmentWrapper(BidgWrapper):
    @BidgWrapper.exterior_set.setter
    def exterior_list(self):
        result = super(ApartmentWrapper, self).exterior_list()[:]
        exclude_set = ('roof')
        for f in exclude_set:
            try:             
                self.result.remove(f)
            except:
                pass               
        return result         
            
class NewapartWrapper(ApartmentWrapper):    
    year_built = u'Год сдачи'    

class HomeWrapper(BidgWrapper):
    pass
class OutbuildingsWrapper(BidgWrapper):
    def __init__(self):
        self.exterior_set = ['year_built', 'floor_count', 'wall_construcion', 'exterior_finish', 'room_count', 'total_area', 'wall_finish', 'flooring', 'interior']
        self.interior_set = []
        self.extra_set = []
    
class SteadWrapper(BaseWrapper):
    field_set = ['estate_type', 'total_area', 'face_area', 'shape', 'land_type', 'purpose']
    #    land_type = u'Земля ТЕСТ'
    
    
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
           }
   
def get_wrapper(obj):    
    if obj.estate_type.template is None:
        raise Exception(u'Не указан шаблон для вида недвижимости %s!' % obj.estate_type)
    if type(obj).__name__ == 'Bidg':
        return WRAPPERS[obj.estate_type.template][0]
    elif type(obj).__name__ == 'Stead':        
        return WRAPPERS[obj.estate_type.template][1]