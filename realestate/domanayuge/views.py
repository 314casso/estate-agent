# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from domanayuge.models import Category
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.utils.encoding import force_unicode
from django.core.mail import EmailMessage
from django.template import loader, Context
from django.contrib.sites.shortcuts import get_current_site
from local_settings import EMAIL_SETTINGS

# Create your views here.

class HomePage(TemplateView):    
    template_name = 'domanayuge/base.html'        
    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
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


@require_http_methods(["POST"])
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