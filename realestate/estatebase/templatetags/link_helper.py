from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def reverse_link(name, *args):
    return reverse(name, args=args)

@register.inclusion_tag('close_btn.html')
def close_btn(url):        
    return {'url': url or ''}

@register.inclusion_tag('contact_list_tag.html')
def contact_list(client, next_url):        
    return {'client': client, 'next_url': next_url}


@register.inclusion_tag('client_list_tag.html')
def client_list(estate, next_url):        
    return {'estate': estate, 'next_url': next_url}

@register.inclusion_tag('address_tag.html')
def address(estate):    
    items = []
    if estate.region:
        items.add(estate.region)
    items.append(estate.locality.name)
    if estate.microdistrict:         
        items.append(estate.microdistrict.name)
    items.append(estate.street.name)                 
    items.append(estate.estate_number)    
    if estate.is_bidg:
        items.append(estate.bidg.bidg_number)        
    address = ', '.join(items)
    return {'address': address}