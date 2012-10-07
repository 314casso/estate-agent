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
    field_set = None    
    def __init__(self):
        for f in self.get_exclude_set():
            try:             
                self.field_set.remove(f)
            except:
                pass              
    def field_list(self):                
        return self.field_set
    def interior_list(self):
        return self.interior_set
    def get_exclude_set(self):
        return []
               
class BidgWrapper(BaseWrapper):    
    field_set = ['estate_type', 'room_number', 'year_built', 'floor', 'floor_count', 'elevator', 'wall_construcion', 'exterior_finish', 'window_type', 'roof', 'heating', 'ceiling_height', 'room_count', 'total_area', 'used_area', 'wall_finish', 'flooring', 'ceiling', 'interior', 'basic']    
    interior_set = ['wall_finish', 'flooring', 'ceiling', 'interior']
    def get_exclude_set(self):        
        exclude_set = super(BidgWrapper, self).get_exclude_set()[:]
        exclude_set.extend(self.interior_list())
        exclude_set.extend(['basic'])                        
        return exclude_set    

class ApartmentWrapper(BidgWrapper):
    def get_exclude_set(self):        
        exclude_set = super(ApartmentWrapper, self).get_exclude_set()[:]        
        exclude_set.extend(['roof'])        
        return exclude_set    

class NewapartWrapper(ApartmentWrapper):
    year_built = u'Год сдачи'    

class HomeWrapper(BidgWrapper):
    pass

class SteadWrapper(BaseWrapper):
    field_set = ['id', 'estate', 'total_area', 'face_area', 'shape', 'land_type', 'purpose']
    #    land_type = u'Земля ТЕСТ'
    def get_exclude_set(self):
        return []
    
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
           OUTBUILDINGS:(None, SteadWrapper()),
           }
   
def get_wrapper(obj):    
    if obj.estate_type.template is None:
        raise Exception(u'Не указан шаблон для вида недвижимости %s!' % obj.estate_type)
    if type(obj).__name__ == 'Bidg':
        return WRAPPERS[obj.estate_type.template][0]
    elif type(obj).__name__ == 'Stead':        
        return WRAPPERS[obj.estate.estate_type.template][1]