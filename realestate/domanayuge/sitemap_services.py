# -*- coding: utf-8 -*-
from django.contrib.sitemaps import GenericSitemap
from domanayuge.sitemaps import StaticViewSitemap

from domanayuge.models import ContentEntry, Category
from django.core.urlresolvers import reverse

def get_blog_dict(tags):
    return {
        'queryset': ContentEntry.objects.filter(categories__slug="blog", tags__contained_by=tags),
        'date_field': 'publication_date',
        }

def get_portfolio_dict(key):
    return {
        'queryset': ContentEntry.objects.filter(categories__key=key),
        'date_field': 'publication_date',
        }

def get_projects_dict(key):
    return {     
        'queryset': ContentEntry.objects.filter(categories__key__in=[cat.key for cat in Category.objects.get(key=key).get_children().all()]),
        'date_field': 'publication_date',
        }

class CaseGenericSitemap(GenericSitemap):
    def location(self, obj):
        return reverse('case', args=[obj.categories.first().pk, obj.slug])
    
class ProjectGenericSitemap(GenericSitemap):
    def location(self, obj):                
        return reverse('project', args=[obj.categories.first().pk, obj.slug])
    

def get_sitemap_dict(tags, portfolio_key, projects_key):    
    return {
      'blog': GenericSitemap(get_blog_dict(tags), priority=0.6),                        
      'static': StaticViewSitemap ,
      'cases': CaseGenericSitemap(get_portfolio_dict(portfolio_key), priority=0.6, ), 
      'projects': ProjectGenericSitemap(get_projects_dict(projects_key), priority=0.6, ),
    }    