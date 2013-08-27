# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.simple_tag            
def separated_list(queryset, fld, sep, ):
    result = []    
    for item in queryset:
        result.append(u'%s' % getattr(item, fld))            
    return sep.join(result)

@register.simple_tag            
def keyval_sep_list(queryset, key, value, sep, delim=':'):
    result = []
    for item in queryset:
        result.append(u'%s%s%s' % (getattr(item, key), delim, getattr(item, value)))            
    return sep.join(result)

@register.simple_tag            
def keyval_sep_feed(queryset, key, value, sep, delim='#'):
    result = []
    for item in queryset:
        name = getattr(item, value)
        name = name.replace('_', '')
        result.append(u'%s%s%s' % (getattr(item, key), delim, name))            
    return '\n'.join(result)    