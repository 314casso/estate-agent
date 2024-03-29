# -*- coding: utf-8 -*-
from django.contrib.sitemaps import GenericSitemap
from domanayuge.models import ContentEntry, Category, SiteMeta, get_all_geo_tags
from django.contrib import sitemaps
from django.core.urlresolvers import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = 'always' # 'daily'
    debugContent = ""
    current_site = "" # should set from outside (in MapPage)
    sitemap_source = None
    linker_ce_sm = {} # reference from ContentEntry to GenericSitemap

    def items(self):
        site_meta = None
        self.debugContent = ""
        self.debugContent += "site=%s" % repr(self.current_site)
        try:
            site_meta = SiteMeta.objects.get(site=self.current_site)
        except SiteMeta.DoesNotExist:
            pass
        self.debugContent += " site_meta=%s" % repr(site_meta)
        geo_tags = site_meta.tags if site_meta else None
        self.debugContent += " geo_tags=%s" % repr(geo_tags)
        qs = []
        if self.sitemap_source:
            for one_generic in self.sitemap_source.generic_sitemap_list:
                for one_record in one_generic.queryset:
                    self.linker_ce_sm[one_record] = one_generic
                    qs.append(one_record)
            self.debugContent += " OUTSIDE WAS SET SITEMAP_SOURCE SIZE=%s" % str(len(qs))
        else:
            qs = ContentEntry.objects.filter(categories__slug="blog")
            if geo_tags:
                qs = qs.filter(tags__contains=geo_tags)
        return qs

    def location(self, item):
        #return '/blog/%s'%(item.slug)
        try:
            if self.linker_ce_sm.get(item):
                return self.linker_ce_sm.get(item).location(item)
        except:
            pass
        return item.get_absolute_url()

    def title(self, item):
        return item.title

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


def get_sitemap_dict(site, tags, portfolio_key, projects_key=None, prices_key=None):
    site_meta = None
    try:    
        site_meta = SiteMeta.objects.get(site=site)
    except SiteMeta.DoesNotExist:
        pass

    geo_tags = site_meta.tags if site_meta else None     
    result = {
      'blog': GenericSitemap(get_blog_dict(tags, geo_tags), priority=0.6),                        
      #'static': StaticViewSitemap,
      'cases': CaseGenericSitemap(get_portfolio_dict(portfolio_key, geo_tags), priority=0.6, ),
    }       
    if projects_key:
        result['projects'] = ProjectGenericSitemap(get_projects_dict(projects_key), priority=0.6, )      
    if prices_key:
        result['prices'] = PriceGenericSitemap(get_projects_dict(prices_key), priority=0.6, )        
    return result