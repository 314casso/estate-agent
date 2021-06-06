# -*- coding: utf-8 -*-
import requests
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template import loader, Context
from django.utils.encoding import force_unicode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView, ContextMixin, View
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
from domanayuge.turbo import FeedGenerator

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


def septik_sitemap(request):    
    site = get_current_site(request)
    return base_sitemap(request, sitemaps=get_sitemap_dict(site, [u'септик'], 'septiktype', None, 'septikprices'))


def rodlex_sitemap(request):    
    site = get_current_site(request)
    return base_sitemap(request, sitemaps=get_sitemap_dict(site, [u'родлекс'], 'rodlextype', None, 'rodlexprices'))


def pogreb_sitemap(request):    
    site = get_current_site(request)
    return base_sitemap(request, sitemaps=get_sitemap_dict(site, [u'погреб'], 'pogrebtype', None, 'pogrebprices'))


def get_terms_use(request):
    return render(request, 'domanayuge/terms-of-use.html')


def get_privacy_policy(request):
    return render(request, 'domanayuge/privacy-policy.html')


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
            'site_meta': self.site_meta,
            'link': self.request.build_absolute_uri(self.request.path)  
        })
                   
        return context
    

class HomePage(BaseContextMixin, TemplateView):   
    tags = [u'недвижимость']
    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)         
        context.update({           
            'articles': ContentEntry.objects.filter(categories__slug=self.blog_slug, tags__overlap=self.tags)[:6],            
        })                          
        return context
    def get_template_names(self):
        turbo = int(self.request.GET.get('turbo', 0))
        if turbo == 1:
            return 'turbo/base.html'
        return 'domanayuge/base.html'             
    
    
class ExContextMixin(ContextMixin):
    blog_slug = 'blog'
    slug = None
    tags = []
    site_meta = None  
    cases_key = None  
    design_key = None
    type_key = None
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
        case_slices = 6        
        articles = ContentEntry.objects.filter(categories__slug=self.blog_slug, tags__overlap=self.tags)
        cases = ContentEntry.objects.filter(categories__key=self.cases_key)        
        designs = ContentEntry.objects.filter(categories__key=self.design_key)
        types = ContentEntry.objects.filter(categories__key=self.type_key)
        
        if geo_tags:            
            articles = articles.filter(tags__contains=geo_tags)           
            cases = cases.filter(tags__contains=geo_tags)            
            designs = designs.filter(tags__contains=geo_tags)
            types = types.filter(tags__contains=geo_tags)
                            
        else:
            ex_tags = get_all_geo_tags()
            if ex_tags:            
                articles = articles.exclude(tags__overlap=ex_tags)
                cases = cases.exclude(tags__overlap=ex_tags)                
                designs = designs.exclude(tags__overlap=ex_tags)
                types = types.exclude(tags__overlap=ex_tags)              
                          
        context.update({           
            'articles': articles[:articles_slices],
            'cases': cases[:case_slices],
            'categiries': categiries,
            'root': root,
            'domain': self.request.domain,
            'site_meta': self.site_meta,
            'designs': designs[:case_slices],            
            'types': types[:case_slices],
        })                            
        return context 
    

class TurboPageMixin(BaseContextMixin, TemplateView):
    template_name = None
    def get_context_data(self, **kwargs):        
        context = super(TurboPageMixin, self).get_context_data(**kwargs)
        context.update({          
            'link': self.request.build_absolute_uri(self.request.path)                
        })        
        return context 
    def get_template_names(self):
        turbo = int(self.request.GET.get('turbo', 0))
        if turbo == 1:
            return 'turbo/base.html'
        return self.template_name      
        
    
class DevContextMixin(ExContextMixin):    
    tags = [u'строительство']
    slug = 'stroyka'          
    cases_key = 'portfoliodev'    

        
class DevPage(DevContextMixin, TurboPageMixin):
    template_name = 'domanayuge/dev.html'      

            
class RemontContextMixin(ExContextMixin):    
    tags = [u'ремонт']
    slug = 'remont'          
    cases_key = 'portfolioremont'
    design_key = 'designremont'


class RemontPage(RemontContextMixin, TurboPageMixin):    
    template_name = 'domanayuge/remont.html'    


class SeptikContextMixin(ExContextMixin):    
    tags = [u'септик']
    slug = 'septik'          
    cases_key = 'portfolioseptik'
    design_key = 'designseptik'
    type_key = 'septiktype'


class RodlexContextMixin(ExContextMixin):    
    tags = [u'родлекс']
    slug = 'rodlex'          
    cases_key = 'portfoliorodlex'
    design_key = 'designrodlex'
    type_key = 'rodlextype'


class PogrebContextMixin(ExContextMixin):    
    tags = [u'погреб']
    slug = 'pogreb'          
    cases_key = 'portfoliopogreb'
    design_key = 'designpogreb'
    type_key = 'pogrebtype'

    
class RodlexPage(RodlexContextMixin, TurboPageMixin):    
    template_name = 'domanayuge/rodlex.html'      
    

class PogrebPage(PogrebContextMixin, TurboPageMixin):    
    template_name = 'domanayuge/pogreb.html'    
    

class SeptikPage(SeptikContextMixin, TurboPageMixin):    
    template_name = 'domanayuge/septik.html'    


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


class VideoBlog(BaseContextMixin, ListView):
    blog_slug = 'videoblog'
    template_name = 'domanayuge/videos.html'
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
    
class SeptikList(SeptikContextMixin, BaseList):    
    template_name = 'domanayuge/projects.html'
    
class RodlexList(RodlexContextMixin, BaseList):    
    template_name = 'domanayuge/projects.html'    
    
class PogrebList(PogrebContextMixin, BaseList):    
    template_name = 'domanayuge/projects.html'    

class CaseList(DevContextMixin, BaseList):
    template_name = 'domanayuge/cases.html'         
    
class DevPriceList(DevContextMixin, BaseList):
    template_name = 'domanayuge/prices.html'
    
class SeptikPriceList(SeptikContextMixin, BaseList):
    template_name = 'domanayuge/prices.html'    
    
class RodlexPriceList(RodlexContextMixin, BaseList):
    template_name = 'domanayuge/prices.html'    
    
class PogrebPriceList(PogrebContextMixin, BaseList):
    template_name = 'domanayuge/prices.html'    
    
class RemontPriceList(RemontContextMixin, BaseList):
    template_name = 'domanayuge/prices.html'   
    
class RemontRenovationServices(RemontContextMixin, BaseList):
    template_name = 'domanayuge/renovationservices.html' 
    
class RemontCaseList(RemontContextMixin, BaseList):
    template_name = 'domanayuge/cases.html'    


class SeptikBaseCaseList(SeptikContextMixin, BaseList):
    template_name = 'domanayuge/cases.html'
    

class SeptikCaseList(SeptikContextMixin, BaseList):
    template_name = 'domanayuge/cases.html'
    def get_queryset(self):
        
        try:                 
            site_meta = SiteMeta.objects.get(site=get_current_site(self.request))
        except SiteMeta.DoesNotExist:
            pass                
        
        geo_tags = site_meta.tags if site_meta else None
                
        key = self.kwargs['key']                   
        cases = ContentEntry.objects.filter(categories__key=key)        
        if geo_tags:          
            cases = cases.filter(tags__contains=geo_tags)            
        else:
            ex_tags = get_all_geo_tags()
            if ex_tags:           
                cases = cases.exclude(tags__overlap=ex_tags)                
        return cases


class RodlexCaseList(RodlexContextMixin, BaseList):
    template_name = 'domanayuge/cases.html'

class PogrebCaseList(PogrebContextMixin, BaseList):
    template_name = 'domanayuge/cases.html'

class DevelopServices(DevContextMixin, BaseList):
    template_name = 'domanayuge/developservices.html'


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
    
    
class SeptikPrice(SeptikContextMixin, BaseEntry):
    template_name = 'domanayuge/price.html'
    context_object_name = 'project'    


class RodlexPrice(RodlexContextMixin, BaseEntry):
    template_name = 'domanayuge/price.html'
    context_object_name = 'project'       

class PogrebPrice(PogrebContextMixin, BaseEntry):
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


class SeptikCase(SeptikContextMixin, BaseEntry):
    template_name = 'domanayuge/case.html'
    context_object_name = 'project'


class RodlexCase(RodlexContextMixin, BaseEntry):
    template_name = 'domanayuge/case.html'
    context_object_name = 'project'

class PogrebCase(PogrebContextMixin, BaseEntry):
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
    
   
    
def turbo(request):
    feed_generator = FeedGenerator()
    return HttpResponse(feed_generator.create_rss(request))  
    
    
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
        
    roistat_data = {
    'roistat' : request.COOKIES.get('roistat_visit', None),
    'key'     : 'MjI2NjU5YmVlNWM0ZWZhYjY2NTY3MzMyNGQ5ZWE0NWI6MTY2NzUy', 
    'title'   : force_unicode('Обращение через сайт'),
    'comment' : force_unicode(request.POST['message']),
    'name'    : force_unicode(request.POST['name']),
    'phone'   : force_unicode(request.POST['phone']),
    'email'   : force_unicode(request.POST['email']),
    'is_need_callback' : '0',
    }  
    
    r = requests.get('https://cloud.roistat.com/api/proxy/1.0/leads/add', params=roistat_data)
    
    return HttpResponse('SUCCESS')
    