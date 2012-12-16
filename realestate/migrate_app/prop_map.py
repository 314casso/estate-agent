# -*- coding: utf-8 -*-
from estatebase.helpers.functions import parse_decimal
from estatebase.models import EstateParam, Document, Bidg, Stead
class PropMap(object):
    _estate = None
    _bidg = None
    _stead = None
    _estate_type = None    
    params= ('comments', 'destination', 'distance', 'electricity_status', 'gas_status', 
    'land_area', 'land_front', 'living_area', 'rooms_count', 'state', 
    'total_area', 'wall_material', 'water_status', 'year_built', 'all_floors', 'apartment_number', 
    'floor', 'phone_status', 'porch_status', 'sewerage_status', 'advertise', 'land_category', 
    'land_distanation', 'land_evidence', 'land_form', 'evidence', 'mortgage', 'internet_status', 
    'heating', 'facing', 'roof', 'windows', 'land_cadastral_number', 'cadastral_number', 'ground', 
    'land_plan', 'technical_certificate', 'wall', 'take_a_photo', 'exchange', 'ceiling_height', 
    'electricity_distance', 'water_distance', 'ceiling', 'gas_distance', 'porch_distance', 'elevator', 
    'sewerage_distance', 'exclusive')    
    
    def __init__(self, estate):
        self.estate = estate        
            
    @property
    def estate(self):
        return self._estate
    
    @estate.setter
    def estate(self, value):
        self._estate = value
        self._bidg = value.basic_bidg
        try:
            self._stead = value.stead
        except Stead.DoesNotExist:
            self._stead = None
        self._estate_type = value._estate_type_id            
        
    @property
    def estate_type(self):
        return self._estate_type
            
    @property    
    def bidg(self):
        if not self._bidg:
            if not self.estate.estate_category.is_stead:
                self._bidg = Bidg.objects.create(estate=self.estate, estate_type_id=self.estate_type, basic=True)
        return self._bidg
   
    @property    
    def stead(self):
        if not self._stead:
            if not self.estate.estate_category.can_has_stead:
                self._stead = Bidg.objects.create(estate=self.estate, estate_type_id=Stead.DEFAULT_TYPE_ID)
        return self._stead    
       
    def get_setter(self, param):
        template = 'set_%s'
        return getattr(self, template % param, None)
    
    def set_param(self, param):
        value = param.value.strip()
        if not value or value == '0':
            return         
#        print 'Call setter %s' % param.name
        param_setter = self.get_setter(param.name)        
        if not param_setter:
            if param.name not in ['old_id', 'correct', 'site']:
                print u'Setter for %s not found!' % param.name
        else:
            try:
                param_setter(param.value)
            except AttributeError:
                print u'%s %s' % (param.name, param.value)
    
    def save_params(self):            
        if self._bidg:
            self._bidg.save()
        if self._stead:
            self._stead.save()    
                    
    def set_comments(self, value):        
        if value:
            if self.estate.comment:                
                self.estate.comment = self.estate.comment + ', ' +  value
            else:
                self.estate.comment = value
    
    def _destination_map(self, value):
        dest_map = {
        u'Азовское море': 2,
        u'Черное море':12,
        u'Курчанский лиман':8,
        u'Таманский залив':10,
        u'лиман Цокур': 11,
        u'озеро Абрау': 1,
        u'Ахтанизовский лиман': 3,
        u'Динской  залив': 5,
        u'Старотитаровский лиман': 9,
        u'Витязевский лиман': 4,
        u'Кизилташский лиман': 6,
        u'река Кубань': 7,
        }
        return dest_map[value] 
    
    def set_destination(self, value):       
        self.estate.beside_id = self._destination_map(value)
    
    def set_distance(self, value):
        self.estate.beside_distance = parse_decimal(value)                       
    
    def set_living_area(self, value):
        self.bidg.used_area = parse_decimal(value)
     
    def set_total_area(self, value):
        self.bidg.total_area = parse_decimal(value)    
    
    def set_rooms_count(self, value):
        self.bidg.room_count = parse_decimal(value)
    
    def set_year_built(self, value):
        int_value = None
        if value:
            try:
                int_value = int(value)
            except:
                return            
        if not 2100 > int_value > 1800:
            return       
        self.bidg.year_built = int_value
    
    def set_all_floors(self, value):        
        self.bidg.floor_count = parse_decimal(value,'/')                   
        
    def set_apartment_number(self, value):         
        self.bidg.room_number = value
    
    def set_floor(self, value):
        self.bidg.floor = parse_decimal(value, splitter='/', index=0)         
    
    def set_ceiling_height(self, value):
        self.bidg.ceiling_height = parse_decimal(value)

    def set_state(self, value):
        state_map = {
        u'1' : None,
        u'без отделки': 1,
        u'ветхое': 2,
        u'евроремонт': 3,
        u'жилое': 4,
        u'капитальный ремонт': 5,
        u'косметический ремонт': 6,
        u'отличное': 7,
        u'предчистовая отделка': 8,
        u'ремонт': 9,
        u'удовлетворительное': 10,
        u'хорошее': 11,
        u'недостроено': 12
        }
        m_val = state_map[value]
        if m_val:
            self.bidg.interior_id = state_map[value]           
    
    def set_wall_material(self, value):
        p_map = {
        u'1': None,
        u'блок': 1,
        u'газоблок': 2,
        u'дерево': 3,
        u'камень': 4,
        u'каркас': 5,
        u'кирпич': 6,
        u'монолит': 7,
        u'панель': 8,
        u'саман': 9,
        u'шлакоблок': 10,
        u'щитовой': 11,
        }
        m_val = p_map[value]
        if m_val:
            self.bidg.wall_construcion_id = p_map[value]
            
    def _status_map(self, value):
        status_map = {
        u'подключено': 5,
        u'подведено': 3,
        u'по меже': 2,
        u'на расстоянии': 1,
        u'технические условия': 6,
        u'подключение оплачено': 4,    
        }       
        return status_map[value]  
    
    def set_electricity_status(self, value):
        self.estate.electricity_id = self._status_map(value)
    
    def set_gas_status(self, value):
        self.estate.gassupply_id = self._status_map(value)         
    
    def set_water_status(self, value):
        p_map = {
        u'водопровод': 1,
        u'колодец': 2,
        u'на расстоянии': 3,
        u'подведено': 5,
        u'подключение оплачено': 6,
        u'подключено': 7,
        u'по меже': 4,
        u'скважина': 8,
        u'технические условия': 9,
        }
        self.estate.watersupply_id = p_map[value] 
        
    def set_phone_status(self, value):
        p_map = {
        u'есть возможность': 1,
        u'нет': 2,
        u'подключено': 3,
        }
        self.estate.telephony_id = p_map[value]

    def set_porch_status(self, value):
        p_map = {
        u'асфальт': 1,
        u'гравийный': 2,
        u'грунтовый': 3,
        u'нет': 4,
        u'хороший': 5,
        }
        self.estate.driveway_id = p_map[value]
        
    def set_sewerage_status(self, value):
        p_map = {
        u'на расстоянии': 1,
        u'подведено': 3,
        u'подключение оплачено': 4,
        u'подключено': 5,
        u'по меже': 2,
        u'септик': 7,
        u'технические условия': 6,
        u'центральная': 8,         
        }
        self.estate.sewerage_id = p_map[value]
        
    def set_internet_status(self, value):
        p_map = {
        u'есть возможность': 1,
        u'нет': 2,
        u'подключено': 3,
        }
        self.estate.internet_id = p_map[value]
        
    def set_electricity_distance(self, value):
        self.estate.electricity_distance = parse_decimal(value)
    
    def set_water_distance(self, value):
        self.estate.watersupply_distance = parse_decimal(value)    
 
    def set_gas_distance(self, value):
        self.estate.gassupply_distance = parse_decimal(value)
    
    def set_porch_distance(self, value):
        self.estate.driveway_distance = parse_decimal(value)

    def set_sewerage_distance(self, value):
        self.estate.sewerage_distance = parse_decimal(value)

    def set_elevator(self, value):
        if value:
            self.bidg.elevator =  True

    def set_ceiling(self, value):
        p_map = {
        u'без отделки': 1,
        u'гипсокартон': 2,
        u'натяжные': 3,
        u'окрашены': 4,
        u'оштукатурены': 5,
        u'пластик': 6,
        u'побелены': 7,
        u'подвесные': 8,
        }
        self.bidg.ceiling_id = p_map[value]

    def set_heating(self, value):
        p_map = {
        u'индивидуальное газовое': 1,
        u'индивидуальное твердотоплевное': 2,
        u'индивидуальное электрическое': 3,
        u'центральное': 4,         
        }        
        self.bidg.heating_id = p_map[value]

    def set_facing(self, value):
        p_map = {
        u'без отделки': 1,
        u'дагестанский камень': 2,
        u'камень': 3,
        u'керамогранит': 4,
        u'кирпич': 5,
        u'короед': 6,
        u'окрашено': 7,
        u'оштукатурено': 8,
        u'плитка': 9,
        u'сайдинг': 10,
        }        
        self.bidg.exterior_finish_id = p_map[value]        
    
    def set_roof(self, value):
        p_map = {
        u'металлопрофиль': 1,
        u'металлочерепица': 2,
        u'мягкая кровля': 3,
        u'ондулин': 4,
        u'оцинкованная сталь': 5,
        u'черепица': 6,
        u'шифер': 7,
        }        
        self.bidg.roof_id = p_map[value]
    
    def set_windows(self, value):
        p_map = {
        u'алюминиевые': 1,
        u'деревянные': 2,
        u'евродерево': 3,
        u'металлопластиковые': 4,
        u'не остеклено': 5,
        }
        self.bidg.window_type_id = p_map[value]
    
    def set_ground(self, value):
        p_map = {
        u'без стяжки': 1,
        u'деревянный': 2,
        u'ковролин': 3,
        u'ламинат': 4,
        u'линолеум': 5,
        u'паркет': 6,
        u'стяжка': 7,
        u'теплый пол': 8,
        }
        self.bidg.flooring_id = p_map[value]
    
    def set_advertise(self, value):
        '''
        Рекламировать
        '''
        if value:
            self.estate.estate_params.add(EstateParam.objects.get(pk=4))
    
    def set_mortgage(self, value):
        '''
        Ипотека
        '''
        if value:
            self.estate.estate_params.add(EstateParam.objects.get(pk=2))       
    
    def set_take_a_photo(self, value):
        '''
        Сделать фото
        '''
        if value:
            self.estate.estate_params.add(EstateParam.objects.get(pk=5))    
    
    def set_exchange(self, value):
        '''
        Обмен
        '''
        if value:
            self.estate.estate_params.add(EstateParam.objects.get(pk=3))        
    
    def set_exclusive(self, value):
        '''
        Эксклюзив
        '''
        if value:
            self.estate.estate_params.add(EstateParam.objects.get(pk=6))
                
    def set_land_area(self, value):
        self.stead.total_area = parse_decimal(value)

    def set_land_front(self, value):
        self.stead.face_area = parse_decimal(value)
    
    def set_land_category(self, value):
        p_map = {
        u'населенных пунктов': 1,
        u'особо охраняемых территорий': 2,
        u'промышленности': 3,
        u'сельскохозяйственного назначения': 4,
        }
        self.stead.land_type_id = p_map[value]
    
    def set_land_distanation(self, value):
        p_map = {
        u'для садоводства и огородничества': 14,
        u'для строительства жилого дома': 15,
        u'для личного подсобного хозяйства': 51,
        u'для коммерческого использования': 20,
        u'сельхозпроизводства': 42,
        }
        self.stead.estate_type_id = p_map[value]
    
    def set_land_form(self, value):
        p_map = {
        u'г-образный': 1,
        u'квадратный': 2,
        u'многогранный': 3,
        u'прямоугольный': 4,
        u'трапециевидный': 5,
        u'треугольный': 6,
        }
        self.stead.shape_id = p_map[value]            
        
    def set_land_evidence(self, value):
        if value:
            self.stead.documents.add(Document.objects.get(pk=7))
    
    def set_evidence(self, value):
        if value:
            self.bidg.documents.add(Document.objects.get(pk=4))    
        
    def set_land_cadastral_number(self, value):
        if value:
            self.stead.documents.add(Document.objects.get(pk=6))
    
    def set_land_plan(self, value):
        if value:
            self.stead.documents.add(Document.objects.get(pk=8))        
        
    def set_cadastral_number(self, value):
        if value:
            self.bidg.documents.add(Document.objects.get(pk=6))
    
    def set_technical_certificate(self, value):
        if value:
            self.bidg.documents.add(Document.objects.get(pk=5))        
   
    def set_wall(self, value):
        p_map = {
        u'без отделки': 1,
        u'гипсокартон': 2,
        u'дерево': 3,
        u'деревянная вагонка': 4,
        u'обои': 5,
        u'окрашены': 6,
        u'оштукатурены': 7,
        u'пластик': 8,
        u'побелены': 9,
        }
        self.bidg.estate_type_id = p_map[value]
        
        

