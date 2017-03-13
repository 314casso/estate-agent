# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView, ContextMixin
from domanayuge.models import Category, ContentEntry
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils.encoding import force_unicode
from django.core.mail import EmailMessage
from django.template import loader, Context
from django.contrib.sites.shortcuts import get_current_site
from local_settings import EMAIL_SETTINGS
from django.views.generic.list import ListView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.detail import DetailView

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
    

class DevPage(BaseContextMixin, TemplateView):    
    template_name = 'domanayuge/dev.html'  
    def get_context_data(self, **kwargs):
        context = super(DevPage, self).get_context_data(**kwargs)         
        context.update({           
            'articles': ContentEntry.objects.filter(categories__slug=self.blog_slug)[:6],            
        })                                   
        context.update({          
            'domain': self.request.domain,
            'test': u'Строительство в {{ locality_loct }}. Для {{ locality_gent }} это хорошо! {{ locality }} лидер!',               
        })             
        return context
    

class Blog(BaseContextMixin, ListView):
    template_name = 'domanayuge/blog.html'
    paginate_by = 10
    def get_queryset(self):           
        return ContentEntry.objects.filter(categories__slug=self.blog_slug)

class Article(BaseContextMixin, DetailView):    
    template_name = 'domanayuge/page.html'
    model = ContentEntry
    context_object_name = 'article'
    def get_context_data(self, **kwargs):
        context = super(Article, self).get_context_data(**kwargs)        
        return context    
       
    
@require_http_methods(["POST"])
@ensure_csrf_cookie
def send_email(request):
    mailto = EMAIL_SETTINGS['domanayuge']    
    t = loader.get_template('domanayuge/email.txt')
    c = Context(request.POST)
    c.update({'site': get_current_site(request)})    
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