# -*- coding: utf-8 -*-
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from estatebase.wrapper import get_wrapper
from collections import OrderedDict
from copy import deepcopy
from estatebase.models import MAYBE
from decimal import Decimal

register = template.Library()

def distance_helper(value):
    if value:
        return u' - %s м' % intcomma(value) 
    return ''

@register.inclusion_tag('inclusion/communication.html')
def communication(estate):
    comms = []
    two_val_template = '%s <strong>%s%s</strong>'
    one_val_template = '%s <strong>%s</strong>'
    if estate.electricity:
        comms.append(two_val_template %  (u'свет', estate.electricity.name.lower(), distance_helper(estate.electricity_distance)))            
    if estate.watersupply:
        comms.append(two_val_template %  (u'вода', estate.watersupply.name.lower(), distance_helper(estate.watersupply_distance)))
    if estate.gassupply:
        comms.append(two_val_template %  (u'газ', estate.gassupply.name.lower(), distance_helper(estate.gassupply_distance)))    
    if estate.sewerage:
        comms.append(two_val_template %  (u'канализация', estate.sewerage.name.lower(), distance_helper(estate.sewerage_distance)))        
    if estate.telephony:
        comms.append(one_val_template %  (u'тел.', estate.telephony.name.lower()))    
    if estate.internet:
        comms.append(one_val_template %  (u'интернет', estate.internet.name.lower()))    
    if estate.driveway:
        comms.append(two_val_template %  (u'подъезд', estate.driveway.name.lower(), distance_helper(estate.driveway_distance)))    
    return {'comms': comms}

@register.inclusion_tag('inclusion/comma_from_details.html')
def wrapper_fieldset_comma(obj, fieldset_name):
    return wrapper_fieldset(obj, fieldset_name)

@register.inclusion_tag('inclusion/tr_from_details.html')
def wrapper_fieldset_tr(obj, fieldset_name):
    return wrapper_fieldset(obj, fieldset_name)

def wrapper_fieldset(obj, fieldset_name):    
    if not obj:
        return ''
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
            
@register.simple_tag            
def estate_details(estate_item):
    result = []    
    if estate_item.beside:
        result.append(u'<label>Расстояние до</label> "%s": %s м.' % (estate_item.beside, estate_item.beside_distance and intcomma(estate_item.beside_distance) or '---'))
    if estate_item.com_status:                    
        status = u'<label>Коммерческое использование:</label> <strong>%s</strong>.' % estate_item.com_status
        result.append(status.lower())     
    return ', '.join(result) 

@register.filter
def to_comma_sep(iterval):
    result = []
    for doc in iterval:
        result.append(doc.name.lower())
    if result:
        return ', '.join(result)
    return u'не готовы'

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
    
    
            
#@register.simple_tag            
#def office_address(region):
            
        
                            