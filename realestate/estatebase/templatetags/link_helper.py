# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from estatebase.models import get_polymorph_label
import base64
from django.contrib.humanize.templatetags.humanize import intcomma


register = template.Library()

@register.simple_tag
def reverse_link(name, *args):
    return reverse(name, args=args)

@register.simple_tag
def next_from_request(next_url):    
    return next_url and ('?next=%s' % next_url.urlencode()) or ''  

@register.simple_tag
def im_source(im):
    return base64.b64encode(im.read())

@register.simple_tag
def selected_css(list_pk,item_pk):
    return (list_pk == item_pk) and 'selected' or '' 

@register.inclusion_tag('inclusion/close_btn.html')
def close_btn(url):        
    return {'url': url or ''}

@register.inclusion_tag('inclusion/table_row.html')
def table_row(queryset,field_name):         
    label = get_label(queryset,field_name)    
    value = get_value(queryset,field_name)           
    return {'field': value, 'label':label }

@register.inclusion_tag('inclusion/inline_field.html')
def inline_field(queryset,field_name):
    return table_row(queryset,field_name)

@register.inclusion_tag('inclusion/contact_list_tag.html')
def contact_list(client, next_url, first=None):
    contacts = client.contacts.all()[:first]
    if first:
        contacts = contacts[:first]    
    return {'contacts': contacts, 'next_url': next_url}

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
    basic_bidg = estate.basic_bidg     
    if basic_bidg and basic_bidg.room_number:
        items.append(u'кв. %s' % basic_bidg.room_number)        
    address = ', '.join(items)
    return {'address': address}

@register.simple_tag
def get_label(queryset,field_name):
    return get_polymorph_label(queryset,field_name) or get_field(queryset, field_name).verbose_name

@register.simple_tag
def get_value(queryset,field_name):
    field = get_field(queryset, field_name)
    value = getattr(queryset,field_name)
    if field.get_internal_type() == 'BooleanField' and value:
        value = u'Есть'
    return value

def get_field(queryset, field_name):
    return queryset._meta.get_field(field_name)

@register.simple_tag
def two_num(n_min, n_max):
    result = ''
    if n_min and n_max:
        if n_min != n_max:     
            result = 'от %s до %s' % (intcomma(n_min),intcomma(n_max))
        else:
            result = '%s' % intcomma(n_max)    
    elif n_min and not n_max:
        result = 'более %s' % (intcomma(n_min))
    elif n_max and not n_min:
        result = 'менее %s' % (intcomma(n_max))
    return result             


