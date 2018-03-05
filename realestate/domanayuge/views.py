# -*- coding: utf-8 -*-
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template import loader, Context
from django.utils.encoding import force_unicode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from domanayuge.models import Category, ContentEntry, SiteMeta, get_all_geo_tags
from local_settings import EMAIL_SETTINGS
from django.shortcuts import render
from django.contrib.sites.models import Site
from django.contrib.sitemaps.views import x_robots_tag

import datetime
from calendar import timegm
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.http import http_date
from domanayuge.sitemaps import get_sitemap_dict

# Create your views here.


@x_robots_tag
def base_sitemap(request, sitemaps, section=None,
            template_name='sitemap.xml', content_type='application/xml'):

    req_protocol = request.scheme
    req_site = get_current_site(request)

    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps = [sitemaps[section]]
    else:
        maps = list(six.itervalues(sitemaps))
    page = request.GET.get("p", 1)

    urls = []
    for site in maps:
        try:
            if callable(site):
                site = site()
            urls.extend(site.get_urls(page=page, site=req_site,
                                      protocol=req_protocol))
        except EmptyPage:
            raise Http404("Page %s empty" % page)
        except PageNotAnInteger:
            raise Http404("No page '%s'" % page)
    response = TemplateResponse(request, template_name, {'urlset': urls},
                                content_type=content_type)
    if hasattr(site, 'latest_lastmod'):
        # if latest_lastmod is defined for site, set header so as
        # ConditionalGetMiddleware is able to send 304 NOT MODIFIED
        lastmod = site.latest_lastmod
        response['Last-Modified'] = http_date(
            timegm(
                lastmod.utctimetuple() if isinstance(lastmod, datetime.datetime)
                else lastmod.timetuple()
            )
        )
    return response


def get_current_site(request):
    if hasattr(request, 'site') and request.site:
        return request.site
    return Site.objects.get_current()


def remont_sitemap(request):    
    site = get_current_site(request)
    return base_sitemap(request, sitemaps=get_sitemap_dict(site, [u'ремонт'], 'portfolioremont', None, 'remontprices'))


def stroyka_sitemap(request):    
    site = get_current_site(request)
    return base_sitemap(request, sitemaps=get_sitemap_dict(site, [u'строительство'], 'portfoliodev', 'projects', 'devprices'))


class BaseContextMixin(ContextMixin): 
    blog_slug = 'blog'
    site_meta = None             
    def get_context_data(self, **kwargs):               
        context = super(BaseContextMixin, self).get_context_data(**kwargs)
        categiries = None        
        try:
            domanayuge = Category.objects.get(slug='domanayuge')
            categiries = domanayuge.get_children().filter(menu=True)
        except Category.DoesNotExist:  # @UndefinedVariable
            pass
        
        try:                 
            self.site_meta = SiteMeta.objects.get(site=get_current_site(self.request))
        except SiteMeta.DoesNotExist:
            pass                          
                                    
        context.update({            
            'categiries': categiries, 
            'root': domanayuge,                    
            'site_meta': self.site_meta  
        })               
        return context
    

class HomePage(BaseContextMixin, TemplateView):    
    template_name = 'domanayuge/base.html'  
    tags = [u'недвижимость']
    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)         
        context.update({           
            'articles': ContentEntry.objects.filter(categories__slug=self.blog_slug, tags__overlap=self.tags)[:6],            
        })                          
        return context          
    
    
class ExContextMixin(ContextMixin):
    blog_slug = 'blog'
    slug = None
    tags = []
    site_meta = None  
    cases_key = None  
    def get_context_data(self, **kwargs):
        context = super(ExContextMixin, self).get_context_data(**kwargs)   
        root = Category.objects.get(slug=self.slug)
        categiries = list(root.get_children().filter(menu=True))
        
        for item in categiries:
            item.idx = item.order
            
        blog = Category.objects.get(slug=self.blog_slug)        
        blog.idx = 350      
        categiries.append(blog)
        categiries.sort(key=lambda x:x.idx)
           
        try:                 
            self.site_meta = SiteMeta.objects.get(site=get_current_site(self.request))
        except SiteMeta.DoesNotExist:
            pass
        
        geo_tags = self.site_meta.tags if self.site_meta else None
        articles_slices = 6
        case_slices = 9        
        articles = ContentEntry.objects.filter(categories__slug=self.blog_slug, tags__overlap=self.tags)
        cases = ContentEntry.objects.filter(categories__key=self.cases_key)                
        if geo_tags:            
            articles = articles.filter(tags__contains=geo_tags)           
            cases = cases.filter(tags__contains=geo_tags)
        else:
            ex_tags = get_all_geo_tags()
            if ex_tags:            
                articles = articles.exclude(tags__overlap=ex_tags)
                cases = cases.exclude(tags__overlap=ex_tags)
                          
        context.update({           
            'articles': articles[:articles_slices],
            'cases': cases[:case_slices],
            'categiries': categiries,
            'root': root,
            'domain': self.request.domain,
            'site_meta': self.site_meta            
        })                                 
        return context 
        
    
class DevContextMixin(ExContextMixin):    
    tags = [u'строительство']
    slug = 'stroyka'          
    cases_key = 'portfoliodev'    
    
    
class DevPage(DevContextMixin, TemplateView):    
    template_name = 'domanayuge/dev.html'  
      
      
class RemontContextMixin(ExContextMixin):    
    tags = [u'ремонт']
    slug = 'remont'          
    cases_key = 'portfolioremont'
    
    
class RemontPage(RemontContextMixin, TemplateView):    
    template_name = 'domanayuge/remont.html'


class Blog(BaseContextMixin, ListView):
    blog_slug = 'blog'
    template_name = 'domanayuge/blog.html'
    paginate_by = 10
    def get_queryset(self):        
        f = {}
        q = ContentEntry.objects.all()
        f['categories__slug'] = self.blog_slug
        if 'tags' in self.request.GET:
            tags = [t.strip() for t in self.request.GET['tags'].split(',')]
            print tags
            f['tags__overlap'] = tags           
        q = q.filter(**f)      
        return q                                 

    
class BaseList(ListView):
    paginate_by = 9    
    def get_queryset(self):
        key = self.kwargs['key']                   
        return ContentEntry.objects.filter(categories__key=key)
    
    def get_context_data(self, **kwargs):
        context = super(BaseList, self).get_context_data(**kwargs)
        context.update({          
            'category': Category.objects.get(key=self.kwargs['key'])                
        })
        return context    


class DevList(DevContextMixin, BaseList):
    template_name = 'domanayuge/projects.html'
            
    
class RemontList(RemontContextMixin, BaseList):    
    template_name = 'domanayuge/projects.html'
    

class CaseList(DevContextMixin, BaseList):
    template_name = 'domanayuge/cases.html'         
    

class DevPriceList(DevContextMixin, BaseList):
    template_name = 'domanayuge/prices.html'
    
    
class RemontPriceList(RemontContextMixin, BaseList):
    template_name = 'domanayuge/prices.html'   

    
class RemontCaseList(RemontContextMixin, BaseList):
    template_name = 'domanayuge/cases.html'    


class Article(BaseContextMixin, DetailView):    
    template_name = 'domanayuge/page.html'
    model = ContentEntry
    context_object_name = 'article'
    def get_context_data(self, **kwargs):
        context = super(Article, self).get_context_data(**kwargs)        
        return context    
       

class BaseEntry(DetailView):    
    model = ContentEntry
    def get_context_data(self, **kwargs):
        context = super(BaseEntry, self).get_context_data(**kwargs)
        context.update({          
            'category': Category.objects.get(key=self.kwargs['key'])                
        })        
        return context


class DevPrice(DevContextMixin, BaseEntry):
    template_name = 'domanayuge/price.html'
    context_object_name = 'project'
       
       
class Project(DevContextMixin, BaseEntry):
    template_name = 'domanayuge/project.html'
    context_object_name = 'project'    


class RemontPrice(RemontContextMixin, BaseEntry):
    template_name = 'domanayuge/price.html'
    context_object_name = 'project'


class Case(DevContextMixin, BaseEntry):
    template_name = 'domanayuge/case.html'
    context_object_name = 'project'


class RemontCase(RemontContextMixin, BaseEntry):
    template_name = 'domanayuge/case.html'
    context_object_name = 'project'

    
def robots(request):
    site = get_current_site(request)
    host = site.domain 
    try:
        site_meta = SiteMeta.objects.get(site=site)
        if site_meta.main_mirror: 
            host = site_meta.main_mirror
    except SiteMeta.DoesNotExist:
        pass
     
    return render(request, 'robots/robots.txt', content_type='text/plain', context={'host': host})
    
    
@require_http_methods(["POST"])
@csrf_exempt
def send_email(request):
    domain = request.domain_pattern if hasattr(request, "domain_pattern") else get_current_site(request) 
    mailto = EMAIL_SETTINGS['domanayuge']    
    t = loader.get_template('domanayuge/email.txt')
    c = Context(request.POST)
    c.update({'site': domain })    
    rendered = t.render(c)
    email = EmailMessage(
        force_unicode('Обращение через сайт'),
        force_unicode(rendered),
        'no-reply@domanayuge.ru',
        mailto, 
        reply_to=[request.POST['email']],        
    )
    email.send(False)
    return HttpResponse('SUCCESS')
    