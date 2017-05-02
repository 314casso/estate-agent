# -*- coding: utf-8 -*-
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template import loader, Context
from django.utils.encoding import force_unicode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from domanayuge.models import Category, ContentEntry
from local_settings import EMAIL_SETTINGS

# Create your views here.

class BaseContextMixin(ContextMixin): 
    blog_slug = 'blog'     
    def get_context_data(self, **kwargs):
        context = super(BaseContextMixin, self).get_context_data(**kwargs)
        categiries = None        
        try:
            domanayuge = Category.objects.get(slug='domanayuge')
            categiries = domanayuge.get_children().filter(menu=True)
        except Category.DoesNotExist:  # @UndefinedVariable
            pass
                                    
        context.update({            
            'categiries': categiries,                      
        })               
        return context
    

class HomePage(BaseContextMixin, TemplateView):    
    template_name = 'domanayuge/base.html'  
    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)         
        context.update({           
            'articles': ContentEntry.objects.filter(categories__slug=self.blog_slug)[:6],            
        })                          
        return context          
    
    
class DevContextMixin(ContextMixin):
    blog_slug = 'blog'
    def get_context_data(self, **kwargs):
        context = super(DevContextMixin, self).get_context_data(**kwargs)   
        stroyka = Category.objects.get(slug='stroyka')
        stroyka_categiries = list(stroyka.get_children().filter(menu=True))
        
        for idx, item in enumerate(stroyka_categiries):
            item.idx = idx * 100
            
        blog = Category.objects.get(slug=self.blog_slug)        
        blog.idx = 250      
        stroyka_categiries.append(blog)
        stroyka_categiries.sort(key=lambda x:x.idx)
                  
        context.update({           
            'articles': ContentEntry.objects.filter(categories__slug=self.blog_slug)[:6],
            'cases': ContentEntry.objects.filter(categories__key='portfoliodev')[:9],
            'stroyka_categiries': stroyka_categiries,            
        })                                   
        context.update({          
            'domain': self.request.domain,           
        })             
        return context    


class DevPage(DevContextMixin, TemplateView):    
    template_name = 'domanayuge/dev.html'  
      

class Blog(BaseContextMixin, ListView):
    blog_slug = 'blog'
    template_name = 'domanayuge/blog.html'
    paginate_by = 10
    def get_queryset(self):           
        return ContentEntry.objects.filter(categories__slug=self.blog_slug)
    

class BaseList(DevContextMixin, ListView):    
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
    
    
class ProjectList(BaseList):
    template_name = 'domanayuge/projects.html'


class CaseList(BaseList):
    template_name = 'domanayuge/cases.html'         
    

class Article(BaseContextMixin, DetailView):    
    template_name = 'domanayuge/page.html'
    model = ContentEntry
    context_object_name = 'article'
    def get_context_data(self, **kwargs):
        context = super(Article, self).get_context_data(**kwargs)        
        return context    
       

class BaseEntry(DevContextMixin, DetailView):    
    model = ContentEntry    
    def get_context_data(self, **kwargs):
        context = super(BaseEntry, self).get_context_data(**kwargs)
        context.update({          
            'category': Category.objects.get(key=self.kwargs['key'])                
        })        
        return context
       
       
class Project(BaseEntry):
    template_name = 'domanayuge/project.html'
    context_object_name = 'project'    


class Case(BaseEntry):
    template_name = 'domanayuge/case.html'
    context_object_name = 'project'
    
    
@require_http_methods(["POST"])
@csrf_exempt
def send_email(request):
    mailto = EMAIL_SETTINGS['domanayuge']    
    t = loader.get_template('domanayuge/email.txt')
    c = Context(request.POST)
    c.update({'site': u"%s" % request.domain })    
    rendered = t.render(c)
    email = EmailMessage(
        force_unicode('Обращение через сайт'),
        force_unicode(rendered),
        request.POST['email'],
        mailto,        
        reply_to=[request.POST['email']],        
    )
    email.send(False)
    return HttpResponse('SUCCESS')    