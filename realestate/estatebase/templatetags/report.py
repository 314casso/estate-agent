# -*- coding: utf-8 -*-
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from estatebase.wrapper import get_wrapper
from collections import OrderedDict

register = template.Library()

def distance_helper(value):
    if value:
        return u' - %s м' % intcomma(value) 
    return ''

@register.inclusion_tag('inclusion/communication.html')
def communication(estate):
    comms = []
    if estate.electricity:
        comms.append('%s: %s%s' %  (u'свет', estate.electricity.name.lower(), distance_helper(estate.electricity_distance)))            
    if estate.watersupply:
        comms.append('%s: %s%s' %  (u'вода', estate.watersupply.name.lower(), distance_helper(estate.watersupply_distance)))
    if estate.gassupply:
        comms.append('%s: %s%s' %  (u'газ', estate.gassupply.name.lower(), distance_helper(estate.gassupply_distance)))    
    if estate.sewerage:
        comms.append('%s: %s%s' %  (u'канализация', estate.sewerage.name.lower(), distance_helper(estate.sewerage_distance)))        
    if estate.telephony:
        comms.append('%s: %s' %  (u'тел.', estate.telephony.name.lower()))    
    if estate.internet:
        comms.append('%s: %s' %  (u'интернет', estate.internet.name.lower()))    
    if estate.driveway:
        comms.append('%s: %s%s' %  (u'подъезд', estate.driveway.name.lower(), distance_helper(estate.driveway_distance)))    
    return {'comms': comms}

@register.inclusion_tag('inclusion/comma_from_details.html')
def wrapper_fieldset_comma(bidg, fieldset_name):
    return wrapper_fieldset(bidg, fieldset_name)

@register.inclusion_tag('inclusion/tr_from_details.html')
def wrapper_fieldset_tr(bidg, fieldset_name):
    return wrapper_fieldset(bidg, fieldset_name)

def wrapper_fieldset(bidg, fieldset_name):
    details = OrderedDict()
    wrapper = get_wrapper(bidg)
    field_list = getattr(wrapper, fieldset_name)    
    for field in field_list:
        bidg_field = bidg._meta.get_field(field)
        value = getattr(bidg,field)
        if bidg_field.get_internal_type() == 'BooleanField' and value:
            value = u'Есть'
        if value:
            details[wrapper.get_label(field) or bidg_field.verbose_name] = value            
    return {'details': details}    