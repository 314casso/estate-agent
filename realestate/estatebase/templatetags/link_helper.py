# -*- coding: utf-8 -*-
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from estatebase.models import EstateClient
import base64
from copy import deepcopy
from django.utils.http import urlencode

register = template.Library()

@register.simple_tag
def im_source(im):
    return base64.b64encode(im.read())

@register.simple_tag
def selected_css(list_pk,item_pk):
    return (list_pk == item_pk) and 'selected' or '' 

@register.inclusion_tag('inclusion/close_btn.html')
def close_btn(url):        
    return {'url': url or ''}

@register.inclusion_tag('inclusion/contact_list_tag.html')
def contact_list(client, next_url, first=None):
    contacts = client.contacts.all()[:first]
    if first:
        contacts = contacts[:first]    
    return {'contacts': contacts, 'next_url': next_url}

@register.inclusion_tag('inclusion/client_list_tag.html')
def client_list(estate, next_url):        
    return {'estate': estate, 'next_url': next_url}

def base_address(estate):    
    items = []
    if estate.region:
        items.append(u'%s район' % estate.region.name)
    if estate.locality:     
        items.append(estate.locality.name)
    if estate.microdistrict:         
        items.append(estate.microdistrict.name)
    return items

@register.simple_tag(takes_context=True)
def address(context, estate):    
    items = deepcopy(base_address(estate))
    user = context.get('request').user
    if not user.has_perm('estatebase.view_private'):
        return ', '.join(items)
    if estate.street:     
        items.append(estate.street.name)
    if estate.estate_number:                      
        items.append(estate.estate_number)        
    basic_bidg = estate.basic_bidg     
    if basic_bidg and basic_bidg.room_number:
        items.append(u'кв. %s' % basic_bidg.room_number)        
    return ', '.join(items)

@register.simple_tag
def no_street_address(estate):
    items = deepcopy(base_address(estate))
    return ', '.join(items)

@register.filter()
def rubble(value):    
    return value and u'%s руб.' % intcomma(value) or ''

@register.simple_tag
def two_num(n_min, n_max):
    result = ''
    if n_min and n_max:
        if n_min != n_max:     
            result = u'от %s до %s' % (intcomma(n_min),intcomma(n_max))
        else:
            result = '%s' % intcomma(n_max)    
    elif n_min and not n_max:
        result = u'более %s' % (intcomma(n_min))
    elif n_max and not n_min:
        result = u'менее %s' % (intcomma(n_max))
    return result             

@register.simple_tag
def estate_client_status(estate_pk,client_pk):
    return EstateClient.objects.get(estate_id=estate_pk,client_id=client_pk).estate_client_status

@register.inclusion_tag('inclusion/history.html')
def history(history):        
    if history:
        return {'history': history}
