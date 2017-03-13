# -*- coding: utf-8 -*-
from django import template
from domanayuge.models import Category, ContentEntry, LocalityDomain
from django.template import Context, Template


register = template.Library()

@register.assignment_tag
def category(slug):
    try:
        return Category.objects.get(slug=slug)
    except Category.DoesNotExist:  # @UndefinedVariable
        return None 
    
@register.assignment_tag
def article(slug):
    try:
        return ContentEntry.objects.get(slug=slug)
    except ContentEntry.DoesNotExist:
        return None
    
@register.filter
def parser(value, domain=None):
    t = Template(value)
    if domain:
        c = Context({
            "locality": domain.locality.name,
            "locality_gent": domain.locality.name_gent,
            "locality_loct": domain.locality.name_loct 
            })
    else:
        doms = LocalityDomain.objects.filter(active=True, in_title=True)
        sep = u', '
        c = Context({
            "locality": sep.join([dom.locality.name for dom in doms]),
            "locality_gent": sep.join([dom.locality.name_gent for dom in doms]),
            "locality_loct": sep.join([dom.locality.name_loct for dom in doms]),
            })        
    return t.render(c) 




    