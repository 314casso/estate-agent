# -*- coding: utf-8 -*-
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from estatebase.wrapper import get_wrapper
from collections import OrderedDict
from copy import deepcopy
from estatebase.models import MAYBE, EntranceEstate
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode

register = template.Library()

def distance_helper(value):
    if value:
        return u' - %s м' % intcomma(value) 
    return ''

def value_helper(fk):
    skip = u'подключено';
    value = fk.name.lower()
    if value != skip:
        return u' %s' % value 
    return ''

@register.inclusion_tag('inclusion/communication.html')
def communication(estate):
    comms = []
    two_val_template = '%s<strong>%s%s</strong>'
    one_val_template = '%s<strong>%s</strong>'
    if estate.electricity:
        comms.append(two_val_template %  (u'свет', value_helper(estate.electricity), distance_helper(estate.electricity_distance)))            
    if estate.watersupply:
        comms.append(two_val_template %  (u'вода', value_helper(estate.watersupply), distance_helper(estate.watersupply_distance)))
    if estate.gassupply:
        comms.append(two_val_template %  (u'газ', value_helper(estate.gassupply), distance_helper(estate.gassupply_distance)))    
    if estate.sewerage:
        comms.append(two_val_template %  (u'канализация', value_helper(estate.sewerage), distance_helper(estate.sewerage_distance)))        
    if estate.telephony:
        comms.append(one_val_template %  (u'тел.', value_helper(estate.telephony)))   
    if estate.internet:
        comms.append(one_val_template %  (u'интернет', value_helper(estate.internet)))    
    if estate.driveway:
        comms.append(two_val_template %  (u'подъезд', value_helper(estate.driveway), distance_helper(estate.driveway_distance)))    
    return {'comms': comms}

@register.inclusion_tag('inclusion/comma_from_details.html')
def wrapper_fieldset_comma(obj, fieldset_name):
    return wrapper_fieldset(obj, fieldset_name)

@register.inclusion_tag('inclusion/tr_from_details.html')
def wrapper_fieldset_tr(obj, fieldset_name):
    return wrapper_fieldset(obj, fieldset_name)

def wrapper_fieldset(obj, fieldset_name):    
    if not obj:
        return {'details': None}
    details = OrderedDict()
    wrapper = get_wrapper(obj)
    if not wrapper:
        return '' 
    field_list = getattr(wrapper, fieldset_name)
    for field in field_list:
        obj_field = obj._meta.get_field(field)
        value = getattr(obj,field)
        if obj_field.get_internal_type() == 'ManyToManyField':
            value = ', '.join(value.all().values_list('name', flat=True)) 
        if obj_field.get_internal_type() == 'BooleanField' and value:
            value = u'Есть'             
        if value:
            #pprint.pprint(vars(obj_field))
            details[wrapper.get_label(field) or obj_field.verbose_name] = value            
    return {'details': details}

@register.inclusion_tag('inclusion/simple_layout.html')
def bidg_layout(level):
    layout_fieldset = OrderedDict([                       
                       ('area', u'%s кв.м'),                         
                       ('layout_feature', '%s'), 
                       ('interior', '%s'),
                       ('furniture', u'мебель - %s'),
                       ('note', '%s')
                       ])   
    layout_dict = OrderedDict()       
    for layout in level.layout_set.all():
        layout_row = OrderedDict()
        for field, label in layout_fieldset.items():
            value = getattr(layout, field)
            if value:
                layout_row[field] = label % value
        layout_dict[layout] = deepcopy(layout_row)         
    return {'layouts': layout_dict}            

@register.inclusion_tag('inclusion/simple_layout_wp.html')
def bidg_layout_wp(level):
    return bidg_layout(level)
            
@register.simple_tag            
def estate_details(estate_item):
    result = []       
    entrances = []
    for entrance in estate_item.entranceestate_set.all():
        entrances.append(entrance.get_human_desc())
    if entrances:
        entrances_str = ', '.join(entrances)
        entrances_str = entrances_str[:1].upper() + entrances_str[1:]        
        result.append(entrances_str) 
    if estate_item.microdistrict:
        microdistrict = u'%s' % estate_item.microdistrict
        result.append(u'%s' % microdistrict.title())
    if estate_item.com_status:
        status = u'%s' % estate_item.com_status                    
        status = u'<br /><label>Коммерческое использование:</label> <strong>%s</strong>' % status.lower() 
        result.append(status)     
    return u'%s.' % '. '.join(result) 

@register.filter
def to_comma_sep(iterval, if_none=u'в процессе'):
    result = []
    for doc in iterval:
        result.append(doc.name.lower())
    if result:
        return ', '.join(result)
    return if_none

@register.simple_tag
def newspaper_address(estate):
    items = []    
    if estate.locality:     
        items.append(estate.locality.name)
    if estate.microdistrict:         
        items.append(estate.microdistrict.name)
    return ', '.join(items) + ', '
            
@register.simple_tag
def show_not_none(value, measure='', pref=''):
    if value:
        return u'%s %s %s' % (pref, value, measure)
    return ''

@register.simple_tag
def floor_compact(bidg):
    result = pref = ''   
    if bidg.floor_count:
        pref = u'этажность'
        result = u'%s' % bidg.floor_count
    if bidg.floor:
        pref =  u'этаж'      
        result = u'%s/%s' % (bidg.floor, result or '---')
    return u'%s %s,' % (pref, result)        

@register.simple_tag
def area_compact(bidg):
    result = pref = '' 
    if bidg.total_area:
        pref = u'общ. пл.'        
        result = u'%s' % bidg.total_area
    if bidg.used_area:       
        pref = u'общ./жил. пл.'       
        result = u'%s/%s' % (result or '---', bidg.used_area)
    return u'%s %s кв.м,' % (pref, result)
    
@register.assignment_tag
def bid_dict(bid):    
    cleaned_data = bid.cleaned_filter
    base = OrderedDict()
    result = OrderedDict()
#     add_to_result(result, u'Код', bid.pk)
#    add_to_result(result, u'Сводный тип', bid.mixed_estate_types)    
    add_to_result(base, u'Статус', comma_set(bid.bid_status.all()))
    add_to_result(base, u'Риэлторы', u', '.join(set([broker.get_full_name() for broker in bid.brokers.all()])))    
    add_to_result(base, u'Источник', u', '.join(set([client.origin.name for client in bid.clients.all() if client.origin])))
    add_to_result(base, u'Цена', int_range_fieled_to_string(cleaned_data.get('agency_price')))
    add_to_result(base, u'Примечание', bid.note)
    
       
    add_to_result(base, u'Коды на осмотр', comma_set(bid.estates.all()))
    add_to_result(base, u'Категории лотов', comma_set(cleaned_data.get('estate_category')))
    add_to_result(base, u'Виды лотов', comma_set(cleaned_data.get('estate_type')))    
    add_to_result(base, u'Ком. статус', cleaned_data.get('com_status'))
    add_to_result(base, u'Районы', comma_set(cleaned_data.get('region')))
    add_to_result(base, u'Населенные пункты', comma_set(cleaned_data.get('locality')))
    add_to_result(base, u'Микрорайоны', comma_set(cleaned_data.get('microdistrict')))
    add_to_result(base, u'Улицы', comma_set(cleaned_data.get('street')))    
    beside = []
    beside_type = cleaned_data.get('beside_type')
    if beside_type:        
        beside.append(dict(EntranceEstate.TYPE_CHOICES).get(int(beside_type)))       
    beside_complex = cleaned_data.get('beside')
    if beside_complex:
        beside.extend(beside_complex)
    beside = [force_unicode(b) for b in beside if b]         
    add_to_result(base, u'Вид/выход', u' '.join(beside))
            
    add_to_result(result, u'Год постройки', int_range_fieled_to_string(cleaned_data.get('year_built')))
    add_to_result(result, u'Этаж', int_range_fieled_to_string(cleaned_data.get('floor')))
    add_to_result(result, u'Этажность', int_range_fieled_to_string(cleaned_data.get('floor_count')))    
    add_to_result(result, u'Материал стен', comma_set(cleaned_data.get('wall_construcion')))
    add_to_result(result, u'Внешняя отделка', comma_set(cleaned_data.get('exterior_finish')))
    add_to_result(result, u'Общая площадь, кв. м', int_range_fieled_to_string(cleaned_data.get('total_area')))
    add_to_result(result, u'Жилая площадь, кв. м', int_range_fieled_to_string(cleaned_data.get('used_area')))
    add_to_result(result, u'Кол-во комнат', int_range_fieled_to_string(cleaned_data.get('room_count')))
    add_to_result(result, u'Состояние', comma_set(cleaned_data.get('interior')))
    add_to_result(result, u'Объекты планировки', comma_set(cleaned_data.get('layouts'), True))
    add_to_result(result, u'Площадь планировки', int_range_fieled_to_string(cleaned_data.get('layout_area')))
    add_to_result(result, u'Постройки', comma_set(cleaned_data.get('outbuildings'), True))
    
    add_to_result(result, u'Площадь уч., кв. м', int_range_fieled_to_string(cleaned_data.get('stead_area')))
    add_to_result(result, u'Фасад, м', int_range_fieled_to_string(cleaned_data.get('face_area')))    
    add_to_result(result, u'Форма', comma_set(cleaned_data.get('shape')))
    add_to_result(result, u'Назначение уч.', comma_set(cleaned_data.get('purposes')))
    
    add_to_result_range = create_range_f(u'%s', u'%s')
    add_to_result_range(result, u'Электричество', cleaned_data.get('electricity'))
    add_to_result_range(result, u'Водоснабжение', cleaned_data.get('watersupply'))
    add_to_result_range(result, u'Газоснабжение', cleaned_data.get('gassupply'))
    add_to_result_range(result, u'Канализация', cleaned_data.get('sewerage'))
    add_to_result_range(result, u'Подъезд', cleaned_data.get('driveway'))        
    return {'base':base, 'details': result}

def create_range_f(v0_t, v1_t):
    def range_f(result, key, value):
        add_to_result(result, key, int_range_fieled_to_string(value, v0_t, v1_t))
    return range_f
    
def add_to_result(result, key, value):
    if value:
        result[key] = value

def int_range_fieled_to_string(values, v0_t=u'от %s', v1_t=u'до %s', splitter=u' ', f=intcomma):
    if not values:
        return    
    result = []  
    if values[0]:
        v0 = f(values[0]) if f else values[0]                                 
        result.append(v0_t % v0) 
    if values[1]:            
        v1 = f(values[1]) if f else values[1] 
        result.append(v1_t % v1)
    if result:
        return  splitter.join(result)
                
def comma_set(values, force_lowcase=False):
    if not values:
        return
    result = u', '.join(set([force_unicode(cat) for cat in values]))
    if force_lowcase:
        result = result.lower()
    return result                            