# -*- coding: utf-8 -*-
from django.contrib.sitemaps import GenericSitemap
from domanayuge.models import ContentEntry, Category, SiteMeta, get_all_geo_tags
from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = 'daily'

    def items(self):        
        return ['blog',]

    def location(self, item):
        return reverse(item)
    
def get_base_dict(q, geo_tags):    
    if geo_tags:
        q = q.filter(tags__contains=geo_tags)        
    else:
        ex_tags = get_all_geo_tags()
        if ex_tags:            
            q = q.exclude(tags__overlap=ex_tags)
    return {
        'queryset': q,
        'date_field': 'publication_date',
        }    
    
def get_blog_dict(tags, geo_tags):
    q = ContentEntry.objects.filter(categories__slug="blog", tags__overlap=tags)
    return get_base_dict(q, geo_tags)

def get_portfolio_dict(key, geo_tags):    
    q = ContentEntry.objects.filter(categories__key=key)
    return get_base_dict(q, geo_tags)

def get_projects_dict(key):
    return {     
        'queryset': ContentEntry.objects.filter(categories__key__in=[cat.key for cat in Category.objects.get(key=key).get_children().all()]),
        'date_field': 'publication_date',
        }

class CaseGenericSitemap(GenericSitemap):  
    def location(self, obj):
        return reverse('case', args=[obj.categories.first().key, obj.slug])
    
class ProjectGenericSitemap(GenericSitemap):
    def location(self, obj):                
        return reverse('project', args=[obj.categories.first().key, obj.slug])
    
class PriceGenericSitemap(GenericSitemap):
    def location(self, obj):                
        return reverse('price', args=[obj.categories.first().key, obj.slug])    


def get_sitemap_dict(tags, portfolio_key, projects_key=None, prices_key=None):
    site_meta = None
    try:    
        site_meta = SiteMeta.objects.get(site=Site.objects.get_current())
    except SiteMeta.DoesNotExist:
        pass
    import logging
    from django.conf import settings
    logger = logging.getLogger('estate')
    logger.error(settings.SITE_ID)

    geo_tags = site_meta.tags if site_meta else None     
    result = {
      'blog': GenericSitemap(get_blog_dict(tags, geo_tags), priority=0.6),                        
      'static': StaticViewSitemap,
      'cases': CaseGenericSitemap(get_portfolio_dict(portfolio_key, geo_tags), priority=0.6, ),
    }       
    if projects_key:
        result['projects'] = ProjectGenericSitemap(get_projects_dict(projects_key), priority=0.6, )      
    if prices_key:
        result['prices'] = PriceGenericSitemap(get_projects_dict(prices_key), priority=0.6, )        
    return result