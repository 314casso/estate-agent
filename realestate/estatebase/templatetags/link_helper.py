# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from estatebase.models import get_polymorph_label

register = template.Library()

@register.simple_tag
def reverse_link(name, *args):
    return reverse(name, args=args)

@register.inclusion_tag('inclusion/close_btn.html')
def close_btn(url):        
    return {'url': url or ''}

@register.inclusion_tag('inclusion/table_row.html')
def table_row(queryset,field_name,template):  
    label = get_label(queryset,field_name,template)
    value = getattr(queryset,field_name)          
    return {'field': value, 'label':label }

@register.inclusion_tag('inclusion/contact_list_tag.html')
def contact_list(client, next_url):        
    return {'client': client, 'next_url': next_url}

@register.inclusion_tag('inclusion/client_list_tag.html')
def client_list(estate, next_url):        
    return {'estate': estate, 'next_url': next_url}

@register.inclusion_tag('inclusion/address_tag.html')
def address(estate):    
    items = []
    if estate.region:
        items.append(estate.region.name)
    items.append(estate.locality.name)
    if estate.microdistrict:         
        items.append(estate.microdistrict.name)
    items.append(estate.street.name)                 
    items.append(estate.estate_number)    
    if estate.basic_bidg and estate.basic_bidg.room_number:
        items.append(u'кв. %s' % estate.basic_bidg.room_number)        
    address = ', '.join(items)
    return {'address': address}

@register.simple_tag
def get_label(queryset,field_name,template):
    return get_polymorph_label(template,field_name) or get_verbose_name(queryset, field_name)            

def get_verbose_name(queryset, field_name):
    return queryset._meta.get_field(field_name).verbose_name
