# -*- coding: utf-8 -*-
from django import template
from domanayuge.models import Category, ContentEntry, LocalityDomain, SiteMeta,\
    get_all_geo_tags
from django.template import Context, Template
from django.core.cache import cache 


register = template.Library()

@register.assignment_tag
def category(key):
    try:
        return Category.objects.get(key=key)
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
            "locality": sep.join(get_unique_localites(doms, 'name')),
            "locality_gent": sep.join(get_unique_localites(doms, 'name_gent')),
            "locality_loct": sep.join(get_unique_localites(doms, 'name_loct')),
            })        
    return t.render(c) 


@register.assignment_tag
def site_filtered(q, site):
    site_meta = None
    try:    
        site_meta = SiteMeta.objects.get(site=site)
    except SiteMeta.DoesNotExist:
        pass
    geo_tags = site_meta.tags if site_meta else None
    
    if geo_tags:
        q = q.filter(tags__contains=geo_tags)        
    else:
        ex_tags = get_all_geo_tags()
        import logging
        logger = logging.getLogger('estate')
        logger.error(u"ex_tags:%s" % ",".join(ex_tags))
        if ex_tags:            
            q = q.exclude(tags__overlap=ex_tags)
    return q


def get_unique_localites(iterable, prop):
    cache_key = 'unique_localites_%s' % prop
    result = cache.get(cache_key)
    if not result:
        result = sorted(list(set([getattr(dom.locality, prop) for dom in iterable])))
        cache.set(cache_key, result, 3600)
    return result
