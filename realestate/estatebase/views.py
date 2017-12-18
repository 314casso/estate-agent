# -*- coding: utf-8 -*-
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, QueryDict
from django.shortcuts import get_object_or_404 , redirect
import json
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, ModelFormMixin, UpdateView, \
    DeleteView, BaseUpdateView, ProcessFormView
from django.views.generic.list import ListView
from estatebase.forms import ClientForm, ContactFormSet, ClientFilterForm, \
    ContactHistoryFormSet, ContactForm, EstateCommunicationForm, EstateParamForm, \
    BidgForm, LevelForm, LevelFormSet, ImageUpdateForm, SteadForm, EstateFilterForm, \
    BidForm, BidFilterForm, BidPicleForm, EstateRegisterForm, \
    EstateRegisterFilterForm, EstateForm, EstateCreateClientForm, EstateCreateForm, \
    ClientStatusUpdateForm, EstateCreateWizardForm, EstateFilterRegisterForm,\
    BidEventForm, BidUpdateForm, FileUpdateForm, EntranceEstateFormSet, GenericLinkFormset ,\
    UserForm
from estatebase.helpers.functions import safe_next_link
from estatebase.models import Estate, Client, EstateType, Contact, Level, \
    EstatePhoto, prepare_history, Stead, Bid, EstateRegister, EstateClient, YES, \
    ExUser, Bidg, BidEvent, BidClient, EstateFile, BidState
from models import EstateTypeCategory
from settings import PUBLIC_MEDIA_URL, LOGIN_REDIRECT_URL
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import escape, escapejs
import urlparse
from django.utils.encoding import smart_str
from wp_helper.models import EstateWordpressMeta,\
    WordpressMetaEstateType, WordpressMetaRegion, WordpressMetaStatus,\
    WordpressTaxonomyTree
from django.contrib.auth.decorators import user_passes_test
import unicodecsv
from estatebase.lib import format_phone, get_validity_delta
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.conf.global_settings import LOGOUT_URL
from devrep.models import Partner
from datetime import datetime, timedelta
from django.http.response import JsonResponse, HttpResponseForbidden
import re
from django.db.models import Q
from django.utils import timezone
from collections import OrderedDict

class BaseMixin(object):
    def get_success_url(self):   
        if '_save' in self.request.POST:     
            return self.request.REQUEST.get('next', '')
        return ''    

class DeleteMixin(SingleObjectMixin):
    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url=LOGOUT_URL, redirect_field_name='nonext'))   
    def dispatch(self, *args, **kwargs):
        return super(DeleteMixin, self).dispatch(*args, **kwargs)
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object._user_id = self.request.user.pk
        self.object.deleted = True
        self.object.save() 
        return HttpResponseRedirect(self.get_success_url())
    
class AjaxMixin(ModelFormMixin):
    def serializer_json(self, data):
        """Returns json format"""
        return json.dumps(data), 'application/json'    

    def no_ajax_response(self):
        return HttpResponse('Waiting for ajax reqiest!')

    def response_alternative(self, form, success=True):
        if success:        
            return HttpResponse(json.dumps({'result': 'success'}))
        else:
            return HttpResponse(json.dumps({'form': form.as_p().replace('\n', ''), 'result': 'error'}))

    def form_valid(self, form):        
        if not self.request.is_ajax():
            return super(AjaxMixin, self).form_valid(form)
        self.object = form.save();
        return self.response_alternative(form)

    def form_invalid(self, form):        
        if not self.request.is_ajax():
            return super(AjaxMixin, self).form_invalid(form)
        return self.response_alternative(form, False)

def upload_images(request):
    if request.method == 'POST':           
        for upfile in request.FILES.getlist('form_file'):
            estate_photo = EstatePhoto(estate_id=request.REQUEST.get('estate', None)) 
            file_content = ContentFile(upfile.read()) 
            estate_photo.image.save(upfile.name, file_content)
            estate_photo.user = request.user
            estate_photo.save()  
            next_url = request.REQUEST.get('next', '')            
    return HttpResponseRedirect(next_url)         

def upload_files(request):
    if request.method == 'POST':           
        object_pk = request.REQUEST.get('object_pk')
        model_key = request.REQUEST.get('model_key')        
        content_object = get_files_content_object(model_key, object_pk)        
        for upfile in request.FILES.getlist('form_file'):                        
            estate_file = EstateFile(content_object=content_object) 
            file_content = ContentFile(upfile.read()) 
            estate_file.file.save(upfile.name, file_content)
            estate_file.name = upfile.name
            estate_file.save()  
            next_url = request.REQUEST.get('next', '')            
    return HttpResponseRedirect(next_url)

class SwapMixin(SingleObjectMixin, View):
    def get_context_data(self, **kwargs):
        context = super(SwapMixin, self).get_context_data(**kwargs)        
        context.update({        
            'next_url': safe_next_link(self.request.get_full_path()),
        })  
    def get(self, request, *args, **kwargs):        
        item = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])        
        try:
            if self.kwargs['direction'] == 'up':
                swap_item = self.get_queryset().filter(order__lt=item.order).order_by('-order')[0]
            else:
                swap_item = self.get_queryset().filter(order__gt=item.order).order_by('order')[0]    
        except IndexError:
            pass
        else:
            self.model.swap(item, swap_item)        
        return HttpResponseRedirect(request.REQUEST.get('next', ''))    

class SwapEstatePhotoView(SwapMixin):
    model = EstatePhoto
    def get_queryset(self):                        
        q = EstatePhoto.objects.filter(estate_id=self.kwargs['estate'])
        return q

class ImageUpdateView(BaseMixin, UpdateView):
    model = EstatePhoto
    template_name = 'image_update.html'
    form_class = ImageUpdateForm
    def get_context_data(self, **kwargs):
        context = super(ImageUpdateView, self).get_context_data(**kwargs)        
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'title': 'Фото',
        })        
        return context    
    
class FileUpdateView(BaseMixin, UpdateView):
    model = EstateFile
    template_name = 'image_update.html'
    form_class = FileUpdateForm
    def get_context_data(self, **kwargs):
        context = super(FileUpdateView, self).get_context_data(**kwargs)        
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'title': 'Файл',
        })        
        return context    
    
class ImageDeleteView(DeleteView):
    model = EstatePhoto
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(ImageDeleteView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Удаление фото...',
            'dialig_body'  : u'Подтвердите удаление фотографии: %s' % self.object,
        })
        return context
    def get_success_url(self):   
        return self.request.REQUEST.get('next', '')                    

class FileDeleteView(DeleteView):
    model = EstateFile
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(FileDeleteView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Удаление файла...',
            'dialig_body'  : u'Подтвердите удаление файла: %s' % self.object,
        })
        return context
    def get_success_url(self):   
        return self.request.REQUEST.get('next', '')

class EstateTypeView(TemplateView):    
    template_name = 'index.html'        
    def get_context_data(self, **kwargs):
        context = super(EstateTypeView, self).get_context_data(**kwargs)                
        estate_categories = EstateTypeCategory.objects.all()
        context.update({
            'title': 'base',
            'estate_categories': estate_categories,
            'next_url': safe_next_link(self.request.get_full_path()),
        })        
        return context 

class EstateTypeViewAjax(TemplateView):
    template_name = 'ajax/estate_type_select.html'
    def get_context_data(self, **kwargs):                
        context = super(EstateTypeViewAjax, self).get_context_data(**kwargs)   
        estate_categories = EstateType.objects.filter(estate_type_category__independent=True).order_by('estate_type_category', 'order')
        context.update({            
            'estate_categories': estate_categories,
        })        
        return context

class PlaceableTypeViewAjax(TemplateView):
    template_name = 'ajax/placeable_select.html'
    def get_context_data(self, **kwargs):
        filter_dict = {}
        category = self.request.GET.get('category', None)
        if category == 'commerce':
            filter_dict.update({
            'estate_type_category__is_commerce' : True
            })
        elif category == 'independent':
            filter_dict.update({
            'estate_type_category__independent' : False
            })             
        estate_categories = EstateType.objects.filter(**filter_dict).select_related().order_by('estate_type_category', 'name')
        context = super(PlaceableTypeViewAjax, self).get_context_data(**kwargs)
        context.update({            
            'estate_categories': estate_categories,
            'estate': self.kwargs['estate'],
        })        
        return context

class EstateMixin(BaseMixin, ModelFormMixin):
    model = Estate
    def get_initial(self):        
        initial = super(EstateMixin, self).get_initial()                    
        initial['_user'] = self.request.user
        return initial   
    def form_valid(self, form):
        self.object = form.save(commit=False)         
        self.object.history = prepare_history(self.object.history, self.request.user.pk)        
        return super(EstateMixin, self).form_valid(form)

class EstateCreateView(EstateMixin, CreateView):
    template_name = 'estate_create.html'       
    form_class = EstateCreateForm    
    def get_initial(self):        
        initial = super(EstateCreateView, self).get_initial()
        if 'estate_type' in self.kwargs:                  
            initial['estate_type'] = self.kwargs['estate_type']        
        initial['estate_status'] = 2
        initial['broker'] = self.request.user           
        return initial
    def get_context_data(self, **kwargs):
        context = super(EstateCreateView, self).get_context_data(**kwargs)        
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
        })        
        return context
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')                                  
        return '%s?%s' % (self.object.detail_link, safe_next_link(next_url))
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        category = form.cleaned_data['estate_type'].estate_type_category
        self.object.estate_category_id = category.pk 
        self.object._estate_type_id = form.cleaned_data['estate_type'].pk
        if category.is_commerce:
            self.object.com_status_id = YES         
        self.object.history = prepare_history(self.object.history, self.request.user.pk)       
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
class EstateCreateClientView(EstateCreateView):
    template_name = 'estate_create.html'       
    form_class = EstateCreateClientForm    
    def get_initial(self):        
        initial = super(EstateCreateClientView, self).get_initial()      
        initial['client'] = self.kwargs.get('client', None)        
        initial['client_status'] = EstateClient.ESTATE_CLIENT_STATUS    
        return initial    
    def form_valid(self, form):
        super(EstateCreateClientView, self).form_valid(form) 
        client = form.cleaned_data.get('client') or None
        estate_client_status = form.cleaned_data.get('client_status') or EstateClient.ESTATE_CLIENT_STATUS
        if client:
            EstateClient.objects.create(client_id=client.pk,
                                        estate_client_status=estate_client_status,
                                        estate=self.object)
        return HttpResponseRedirect(self.get_success_url())    

class EstateCreateWizardView(EstateCreateClientView):
    template_name = 'estate_create.html'       
    form_class = EstateCreateWizardForm
            
class EstateDetailView(DetailView):
    template_name = 'estate_detail.html'    
    def get_queryset(self):                        
        q = Estate.objects.all().select_related()
        return q
    def get_context_data(self, **kwargs):        
        context = super(EstateDetailView, self).get_context_data(**kwargs)
        r = (self.object.agency_price or 0) - (self.object.saler_price or 0)        
        p = float(r) / (self.object.saler_price or 1) * 100              
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'margin': '%s (%s%%)' % (r, int(p)),
            'images': self.object.images.all()[:6],
        })        
        return context
    
class EstateUpdateView(EstateMixin, UpdateView):
    model = Estate
    template_name = 'estate_create.html'
    form_class = EstateForm
    def get_context_data(self, **kwargs):
        context = super(EstateUpdateView, self).get_context_data(**kwargs)        
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'estate_type': self.object.estate_type,
        })        
        return context       

class EstateDeleteView(DeleteMixin, EstateMixin, DeleteView):
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(EstateDeleteView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Удаление лота в корзину...',
            'dialig_body'  : u'Подтвердите удаление лота: [%s]' % self.object,
        })
        return context
    def get_success_url(self):   
        return self.request.REQUEST.get('next', '')

class EstateCommunicationUpdateView(EstateUpdateView):
    template_name = 'estate_comm.html'
    form_class = EstateCommunicationForm

class EstateParamUpdateView(EstateUpdateView):    
    template_name = 'estate_params.html'
    form_class = EstateParamForm

def set_estate_filter(q, filter_dict, force_valid=False, user=None, force_delta=False):
    if 'Q' in filter_dict:
        q = q.filter(filter_dict.pop('Q'))
    if force_valid:
        filter_dict.update({
           'validity_id' : Estate.VALID,
        })
    if force_delta:        
        filter_dict.update({           
            'history__modificated__gt' : get_validity_delta(),
        })
    if user:
        filter_dict.update({'region__geo_group__userprofile__user__exact': user })  
    if len(filter_dict):
        q = q.filter(**filter_dict)
        if 'images__isnull' in filter_dict:
            if not filter_dict['images__isnull']:
                return q.distinct('id')
    return q.distinct()

class EstateListView(ListView):    
    filtered = False
    template_name = 'estate_list.html'
    paginate_by = 25  
    filter_form = EstateFilterForm
    def get_queryset(self):
        #q = Estate.objects.select_related('region','locality','microdistrict','street','estate_type','history','estate_status','contact__contact_state','contact__contact_type','contact__client__client_type')
        q = Estate.objects.select_related().prefetch_related('bidgs__estate_type__estate_type_category', 'history')        
        filter_form = self.filter_form(self.request.GET)
        filter_dict = filter_form.get_filter()        
        if filter_dict:
            self.filtered = True                    
        q = set_estate_filter(q, filter_dict, user=self.request.user)
        order_by = self.request.fields 
        if order_by:      
            return q.order_by(','.join(order_by))
        return q
    def get_context_data(self, **kwargs):
        context = super(EstateListView, self).get_context_data(**kwargs)
        filter_form = self.filter_form(self.request.GET)
        
        params = self.request.GET.copy()      
        get_params = params.urlencode()
                   
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'total_count': Estate.objects.count(),
            'filter_count' : self.get_queryset().count(),
            'filter_form': filter_form,
            'filter_action': '%s?next=%s' % (reverse('estate-list'), self.request.GET.get('next','')),
            'filtered' :self.filtered,
            'get_params': get_params,
        })        
        return context
       
class EstateListDetailsView(EstateListView):   
    paginate_by = 7 
    template_name = 'estate_list.html'
    estate = None 
    def get_context_data(self, **kwargs):        
        context = super(EstateListDetailsView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', None)
        try:
            if pk:
                self.estate = self.get_queryset().filter(id=pk)[:1].get()
        except Estate.DoesNotExist:
            self.estate = None
        r = p = 0
        if self.estate:      
            r = (self.estate.agency_price or 0) - (self.estate.saler_price or 0)        
            p = float(r) / (self.estate.saler_price or 1) * 100                                           
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'margin': '%s (~%s%%)' % (intcomma(r), int(p)),
            'images': self.estate and self.estate.images.all()[:6] or None,
            'files': self.estate and self.estate.files.all()[:6] or None,
            'links': self.estate and self.estate.links.all()[:6] or None,
            'estate': self.estate,
        })                
        return context        

class EstateSelectRegisterView(EstateListDetailsView):
    filter_form = EstateFilterRegisterForm    
    def get_queryset(self):
        r_filter = self.request.GET.get('r_filter', None)
        self.register = get_object_or_404(EstateRegister, pk=self.kwargs['selected'])                  
        q = super(EstateSelectRegisterView, self).get_queryset()
        if not r_filter:
            return q
        estates_in_register = list(self.register.estates.all().values_list('id', flat=True))
        pk = int(self.kwargs.get('pk', 0))
        if r_filter == 'inregister':
            if pk and pk not in estates_in_register:
                estates_in_register.append(pk)
            q = q.filter(id__in=estates_in_register)
        else:
            if pk in estates_in_register:
                estates_in_register.remove(pk)
            q = q.exclude(id__in=estates_in_register)
        return q
    def get_context_data(self, **kwargs):
        context = super(EstateSelectRegisterView, self).get_context_data(**kwargs)
        selected = self.kwargs['selected']
        in_register = False
        if self.estate and self.estate.estate_registers.filter(pk=selected):
            in_register = True
        context.update({            
            'selected': selected,
            'filter_action': '%s?next=%s&r_filter=%s' % (reverse('estate_select_list', kwargs={'selected': selected}), self.request.GET.get('next',''), self.request.GET.get('r_filter','')),
            'in_register': in_register,
            'register' : self.register,
        })
        return context

class EstateImagesView(TemplateView): 
    template_name = 'estate_images.html'
    def get_context_data(self, **kwargs):
        context = super(EstateImagesView, self).get_context_data(**kwargs)        
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'estate': Estate.objects.get(pk=kwargs['estate'])            
        })        
        return context      

def get_files_model(model_key):
    model_keys = {'estate':Estate, 'bid': Bid, 'partner': Partner}
    return model_keys.get(model_key)

def get_files_content_object(model_key, object_pk):
    files_model = get_files_model(model_key)
    return files_model.objects.get(pk=object_pk)

class GenericFilesView(TemplateView): 
    template_name = 'generic_files.html'    
    def get_context_data(self, **kwargs):
        model_key = kwargs['model_key']        
        content_object = get_files_content_object(model_key, kwargs['object_pk'])        
        context = super(GenericFilesView, self).get_context_data(**kwargs)                 
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),            
            'content_object': content_object,            
            'model_key': model_key,
        })        
        return context

class GenericLinksView(GenericFilesView): 
    template_name = 'generic_links.html'    

class ClientUpdateEstateView(DetailView):   
    model = Client
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(ClientUpdateEstateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Привязка...',
            'dialig_body'  : u'Привязать заказчика %s к объекту [%s]?' % (self.object, self.kwargs['estate_pk']),
        })
        return context
    def update_object(self, client_pk, estate_pk):
        '''
        Вынесена для переопределения в потомках класса
        '''        
        EstateClient.objects.create(client_id=client_pk, estate_id=estate_pk,
                                    estate_client_status_id=EstateClient.ESTATE_CLIENT_STATUS)                
    def post(self, request, *args, **kwargs):       
        self.update_object(self.kwargs['pk'], self.kwargs['estate_pk'])       
        #Обновление истории и контакта у оъекта                            
        prepare_history(Estate.objects.get(pk=self.kwargs['estate_pk']).history, self.request.user.pk)      
        return HttpResponseRedirect(self.request.REQUEST.get('next', ''))    

class ClientRemoveEstateView(ClientUpdateEstateView):    
    def get_context_data(self, **kwargs):
        context = super(ClientRemoveEstateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Отвязка...',
            'dialig_body'  : u'Отвязать заказчика %s от объекта [%s]?' % (self.object, self.kwargs['estate_pk']),
        })
        return context 
    def update_object(self, client_pk, estate_pk):
        EstateClient.objects.get(estate_id=estate_pk, client_id=client_pk).delete()                   
        
class ObjectMixin(ModelFormMixin):    
    model = Bidg    
    continue_url = None    
    def form_valid(self, form):
        prepare_history(self.get_estate().history, self.request.user.pk)       
        return super(ObjectMixin, self).form_valid(form)    
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')         
        if '_continue' in self.request.POST:                  
            return '%s?%s' % (reverse(self.continue_url, args=[self.object.id]), safe_next_link(next_url)) 
        return next_url
    def get_estate(self):
        return self.object and self.object.estate or Estate.objects.get(pk=self.kwargs['estate'])            
    def get_context_data(self, **kwargs):
        context = super(ObjectMixin, self).get_context_data(**kwargs)        
        context.update({            
            'estate': self.get_estate(),
        })        
        return context

class ApartmentCreateView(ObjectMixin, CreateView):
    template_name = 'bidg_form.html'        
    form_class = BidgForm   
    continue_url = 'apartment_update'
    def get_initial(self):        
        initial = super(ApartmentCreateView, self).get_initial()                
        initial['estate'] = self.kwargs['estate']
        return initial

class ApartmentUpdateView(ObjectMixin, UpdateView):
    template_name = 'bidg_form.html'        
    form_class = BidgForm   
    continue_url = 'apartment_update'        

class ClientListView(ListView):
    template_name = 'clients/client_list.html'
    context_object_name = "clients"
    paginate_by = 20
    filtered = False    
    def get_queryset(self):                        
        q = Client.objects.select_related().prefetch_related('origin', 'contacts__contact_state', 'contacts__contact_type')
        search_form = ClientFilterForm(self.request.GET)
        filter_dict = search_form.get_filter()
        if filter_dict:
            self.filtered = True
        if 'Q' in filter_dict:
            q = q.filter(filter_dict.pop('Q'))
        if len(filter_dict):
            q = q.filter(**filter_dict)        
        order_by = self.request.fields 
        if order_by:      
            return q.order_by(','.join(order_by))
        return q    
    def get_context_data(self, **kwargs):        
        try:
            context = super(ClientListView, self).get_context_data(**kwargs)
        except Http404:
            self.kwargs['page'] = 'last'
            context = super(ClientListView, self).get_context_data(**kwargs)                  
        context.update ({        
            'title': 'list',
            'next_url': safe_next_link(self.request.get_full_path()),
            'client_filter_form' : ClientFilterForm(self.request.GET),
            'filtered': self.filtered,
            'get_params' : self.request.GET.copy().urlencode(),
            
        })        
        return context

class ClientSelectView(ClientListView):
    template_name = 'clients/client_select.html'
    def get_estate(self):
        estate = Estate.objects.get(pk=self.kwargs['estate_pk'])
        return estate            
    def get_context_data(self, **kwargs):         
        context = super(ClientSelectView, self).get_context_data(**kwargs)                    
        context.update ({            
            'estate' : self.get_estate(),
            'client_filter_form' : ClientFilterForm(self.request.GET),
        })        
        return context
    def get_queryset(self):
        q = super(ClientSelectView, self).get_queryset()
        q = q.exclude(estates__id=self.kwargs['estate_pk'])
        return q   
    
class ClientBidSelectView(ClientListView):
    template_name = 'clients/client_bid_select.html'
    def get_bid(self):
        bid = Bid.objects.get(pk=self.kwargs['bid_pk'])
        return bid            
    def get_context_data(self, **kwargs):         
        context = super(ClientBidSelectView, self).get_context_data(**kwargs)                    
        context.update ({            
            'bid' : self.get_bid(),
            'client_filter_form' : ClientFilterForm(self.request.GET),
        })        
        return context
    def get_queryset(self):
        q = super(ClientBidSelectView, self).get_queryset()
        q = q.exclude(bids_m2m__id=self.kwargs['bid_pk'])
        return q

class ClientMixin(ModelFormMixin):
    template_name = 'clients/client_form.html'
    model = Client
    form_class = ClientForm          
    def form_valid(self, form):
        context = self.get_context_data()
        contact_form = context['contact_formset']
        if contact_form.is_valid():            
            self.object = form.save(commit=False)             
            self.object.history = prepare_history(self.object.history, self.request.user.pk)
            self.object.save()            
            if contact_form.has_changed():                
                contact_form.instance = self.object
                contacts = contact_form.save(commit=False)
                for contact in contacts:
                    contact.user_id = self.request.user.pk                    
                contact_form.save()
            if  '_popup' in self.request.POST:            
                return HttpResponse(
                '<!DOCTYPE html><html><head><title></title></head><body>'
                '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script></body></html>' % \
                (escape(self.object.pk), escapejs(self.object)))                                               
            return super(ModelFormMixin, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form,contact_formset=contact_form))
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')                  
        if '_continue' in self.request.POST:                  
            return '%s?%s' % (reverse('client_update', args=[self.object.id]), safe_next_link(next_url))
        return next_url
    def get_context_data(self, **kwargs):
        context = super(ClientMixin, self).get_context_data(**kwargs)                
        if self.request.POST:
            if not 'contact_formset' in context:
                context['contact_formset'] = ContactFormSet(self.request.POST, instance=self.object)   
        else:
            context['contact_formset'] = ContactFormSet(instance=self.object)
        return context                        

class ClientCreateView(ClientMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super(ClientCreateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Добавление нового заказчика'
        })        
        return context    
    def get_initial(self):        
        initial = super(ClientCreateView, self).get_initial()
        initial['broker'] = self.request.user.pk        
        return initial
      
class ClientUpdateView(ClientMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Редактирование заказчика [%s] «%s»' % (self.object.pk, self.object) 
        })        
        return context

class ClientDeleteView(DeleteMixin, ClientMixin, DeleteView):
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(ClientDeleteView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Удаление заказчика...',
            'dialig_body'  : u'Подтвердите удаление заказчика: %s' % self.object,
        })
        return context     
    
class ContactMixin(BaseMixin):
    model = Contact       
    
class ContactHistoryListView(ContactMixin, DetailView):
    '''  
    Пока не используется    
    '''    
    template_name = 'contact_history_list.html'        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = ContactHistoryFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()                        
            return HttpResponseRedirect(self.get_success_url())                
        else:
            return self.render_to_response(self.get_context_data())
        
    def get_context_data(self, **kwargs): 
        context = super(ContactHistoryListView, self).get_context_data(**kwargs)        
        if self.request.POST:
            context['history_formset'] = ContactHistoryFormSet(self.request.POST, instance=self.object)            
        else:
            context['history_formset'] = ContactHistoryFormSet(instance=self.object)                
        context.update ({        
            'title': 'История контакта %s' % self.object,
            'next_url': safe_next_link(self.request.get_full_path()),
        })        
        return context
      
class ContactUpdateView(ContactMixin, UpdateView):    
    template_name = 'contact_update.html' 
    form_class = ContactForm
    def get_context_data(self, **kwargs): 
        context = super(ContactUpdateView, self).get_context_data(**kwargs)                        
        context.update ({        
            'title': 'Редактирование контакта %s' % self.object,
            'next_url': safe_next_link(self.request.get_full_path()),
        })        
        return context
    def form_valid(self, form):            
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.pk              
        prepare_history(self.object.client.history, self.request.user.pk)  
        return super(ContactUpdateView, self).form_valid(form)               
        
    
class LevelMixin(ModelFormMixin):
    template_name = 'layout_update.html'
    form_class = LevelForm
    model = Level
    def get_context_data(self, **kwargs):
        if 'bidg' in self.kwargs:
            bidg = Bidg.objects.get(pk=self.kwargs['bidg'])
        else:
            bidg = self.object.bidg                
        context = super(LevelMixin, self).get_context_data(**kwargs)
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'bidg': bidg,
        })                        
        if self.request.POST:
            context['layout_formset'] = LevelFormSet(self.request.POST, instance=self.object)            
        else:
            context['layout_formset'] = LevelFormSet(instance=self.object)
        return context  
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')         
        if '_continue' in self.request.POST:                  
            return '%s?%s' % (reverse('level_update', args=[self.object.id]), safe_next_link(next_url)) 
        return next_url
    def form_valid(self, form):
        context = self.get_context_data()
        layout_form = context['layout_formset']
        if layout_form.is_valid():
            self.object = form.save(commit=False)                         
            self.object.save()             
            layout_form.instance = self.object            
            layout_form.save()
            #Обновление истории объекта                                 
            prepare_history(self.object.bidg.estate.history, ExUser.objects.get(pk=self.request.user.pk))
            return super(ModelFormMixin, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class LevelCreateView(LevelMixin, CreateView):
    def get_initial(self):        
        initial = super(LevelCreateView, self).get_initial()                
        initial['bidg'] = self.kwargs['bidg']
        return initial

class LevelUpdateView(LevelMixin, UpdateView):
    pass
    
class LevelDeleteView(LevelMixin, DeleteView):
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(LevelDeleteView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Удаление уровня планировки...',
            'dialig_body'  : u'Подтвердите удаление уровня: %s' % self.object,
        })
        return context    

class SteadUpdateView(ObjectMixin, UpdateView):    
    model = Stead
    template_name = 'stead_form.html'        
    form_class = SteadForm   
    continue_url = 'stead_update'
    def get_form(self, form_class):
        form = super(SteadUpdateView, self).get_form(form_class)
        form.user = self.request.user
        return form

class BidgAppendView(TemplateView):    
    template_name = 'confirm.html'
    dialig_title = u'Добавление строения или сооружения...'
    dialig_body = u'Добавить строение или сооружение на участок?'    
    def get_context_data(self, **kwargs):        
        context = super(BidgAppendView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : self.dialig_title,
            'dialig_body'  : self.dialig_body,
        })
        return context
    def update_object(self):
        '''
        Вынесена для переопределения в потомках класса
        '''        
        bidg = Bidg(estate_id=self.kwargs['estate'], estate_type_id=self.kwargs['estate_type'])
        bidg.save()
        self.estate = bidg.estate     
    def post(self, request, *args, **kwargs):        
        self.update_object()
        user = ExUser.objects.get(pk=self.request.user.pk)        
        #Обновление истории объекта        
        prepare_history(self.estate.history, user)
        return HttpResponseRedirect(self.request.REQUEST.get('next', ''))      
    
class BidgRemoveView(BidgAppendView):
    dialig_title = u'Удаление строения или сооружения...'
    dialig_body = u'Удалить строение или сооружение с участка?'
    def update_object(self):                        
        bidg = Bidg.objects.get(pk=self.kwargs['pk'])
        self.estate = bidg.estate
        bidg.delete();        

class SteadAppendView(BidgAppendView):
    dialig_title = u'Добавление участка...'
    dialig_body = u'Добавить участок к лоту?'
    def update_object(self):   
        stead = Stead(estate_id=self.kwargs['estate'])
        stead.save()
        self.estate = stead.estate

class SteadRemoveView(BidgAppendView):
    dialig_title = u'Удаление участка...'
    dialig_body = u'Удалить участок из лота?'
    def update_object(self):   
        stead = Stead.objects.get(pk=self.kwargs['pk'])
        self.estate = stead.estate
        stead.delete();

class BidMixin(ModelFormMixin):
    template_name = 'bid_update.html'
    form_class = BidForm
    model = Bid  
    
    def get(self, request, *args, **kwargs):        
        self.object = self.get_object()
        user = request.user                
        if self.object and user and not user.has_perm('estatebase.view_other_bid'):
            state = self.object.get_state()             
            if not (self.object.brokers.filter(id=request.user.pk) or state.is_expired or
                state.state in [BidState.FREE,BidState.NEW,BidState.PENDING]):                       
                return HttpResponseForbidden()
        return super(BidMixin, self).get(self, request, *args, **kwargs)
      
    def get_context_data(self, **kwargs):
        client = None
        if 'client' in self.kwargs:
            client = Client.objects.get(pk=self.kwargs['client'])
        elif self.object:
            client = self.object.client                 
        context = super(BidMixin, self).get_context_data(**kwargs)
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'client': client,
        })       
        if self.request.POST:
            context['estate_filter_form'] = BidPicleForm(self.request.POST)            
        else:           
            bf = BidPicleForm(initial=self.object.cleaned_filter if self.object else None)            
            context['estate_filter_form'] = bf                       
        return context  
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')         
        if '_continue' in self.request.POST:                  
            return '%s?%s' % (reverse('bid_update', args=[self.object.id]), safe_next_link(next_url)) 
        return next_url
    def form_valid(self, form):
        context = self.get_context_data()
        estate_filter_form = context['estate_filter_form']
        if estate_filter_form.is_valid():
            self.object = form.save()                      
            # Запаковываем фильтр в поле
            cleaned_data = estate_filter_form.cleaned_data
            self.object.cleaned_filter = cleaned_data                        
            self.object.history = prepare_history(self.object.history, self.request.user.pk)            
            self.object.save()            
            return super(ModelFormMixin, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))    

class BidCreateView(BidMixin, CreateView):
    def get(self, request, *args, **kwargs):
        return super(CreateView, self).get(self, request, *args, **kwargs)

    def get_initial(self):        
        initial = super(BidCreateView, self).get_initial()
        if 'client' in self.kwargs:
            client_pk = self.kwargs['client']
            if not Client.objects.filter(pk=client_pk).exists():
                raise Exception(u'Заказчик с id %s не найден!' % client_pk)                
            initial['client'] = client_pk
        initial['broker'] = self.request.user.pk
        return initial
    def form_valid(self, form):
        result = super(BidCreateView, self).form_valid(form)
        if self.object:
            client = form.cleaned_data.get('client') or None        
            if client:
                BidClient.objects.create(client=client, bid=self.object)
        return result


class BidUpdateView(BidMixin, UpdateView):    
    form_class = BidUpdateForm


class BidDeleteView(DeleteMixin, BidMixin, DeleteView):
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(BidDeleteView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Удаление заявки...',
            'dialig_body'  : u'Подтвердите удаление заявки: %s' % self.object,
        })
        return context    


class BidDetailView(BidMixin, DetailView):
    template_name = 'bid_detail.html'
           
    def get_context_data(self, **kwargs):
        context = super(BidDetailView, self).get_context_data(**kwargs)
        q = self.object.estate_registers.all()
        order_by = self.request.fields
        if order_by:      
            q = q.order_by(','.join(order_by))
        context.update({
                'register_list' : q             
                })
        return context 


class BidListView(ListView):
    view_pk = 'bidlist'
    filtered = False    
    template_name = 'bid_list.html'
    paginate_by = 7 
    _bid_count = None  
    _filter_count = None
    available_views = OrderedDict([('bidlist', {'title': u'Все заявки', 'url':'bid-list'}), 
                                   ('bidfreelist', {'title': u'Свободные заявки', 'url':'bid-free-list'})])
    
    def extra_filter(self, q, user):
        if not user.has_perm('estatebase.view_other_bid'):
            self.available_views['bidlist']['title'] = u'Мои заявки'           
            q = q.filter(brokers=user)
        return q
    
    def get_queryset(self):
        user = self.request.user
        q = Bid.objects.prefetch_related('brokers', 'clients')                                          
        search_form = BidFilterForm(self.request.GET)
        filter_dict = search_form.get_filter()
        if filter_dict:
            self.filtered = True
        
        geo_list = set(user.userprofile.geo_groups.values_list('id', flat=True))                            
        q = q.filter(geo_groups__id__in=geo_list)
        
        q = self.extra_filter(q, user)        
                
        if len(filter_dict):
            if 'Q' in filter_dict:
                q = q.filter(filter_dict.pop('Q'))
            if 'E' in filter_dict:                
                q = q.exclude(**filter_dict.pop('E'))
            q = q.filter(**filter_dict)            
        order_by = self.request.fields 
        if order_by:      
            q = q.order_by(','.join(order_by))            
        q = q.distinct()
        q = q.defer('estate_filter', 'cleaned_filter', 'note')        
        return q
    def get_context_data(self, **kwargs):
        context = super(BidListView, self).get_context_data(**kwargs)
        bid_filter_form = BidFilterForm(self.request.GET)
        params = self.request.GET.copy()    
        params_no_page = self.request.GET.copy()
        if 'page' in params_no_page:
            del(params_no_page['page'])                                                                               
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'bid_count': self.get_bid_count(),
            'bid_filter_form': bid_filter_form,
            'filtered': self.filtered,            
            'filter_count' : self.get_filter_count(),
            'get_params' : params.urlencode(),
            'params_no_page': params_no_page.urlencode(),
            'view_pk': self.view_pk,
            'available_views': self.available_views
        })        
        return context
        
    def get_bid_count(self):
        if self._bid_count is None:
            self._bid_count = Bid.objects.count()        
        return self._bid_count
    
    def get_filter_count(self):
        if self._filter_count is None:
            self._filter_count = self.get_queryset().count()        
        return self._filter_count


class BidFreeListView(BidListView):
    view_pk = 'bidfreelist'    
    def extra_filter(self, q, user):        
        q = q.filter(
                    Q(state__state__in=[BidState.WORKING], state__event_date__lt=BidState.get_free_date()) |
                    Q(state__state__in=[BidState.FREE,BidState.NEW])
                    )
        return q
    
                
def bid_calendar_events(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    ids = request.GET.getlist('ids[]')
    users = [request.user.id]
    if ids:
        users = [int(x) for x in ids]
        
    q = BidEvent.objects.filter(Q(bid__brokers__id__in=users) | Q(history__created_by__id__in=users))    
    q = q.filter(bid_event_category__is_calendar=True, date__range=(start, end))
    q = q.exclude(bid__state__state__in=[BidState.CLOSED])
    dicts = [ obj.as_dict() for obj in q.distinct() ]     
    return JsonResponse(dicts, safe=False)


def events_calendar(request):
    form = None
    if request.user.has_perm('estatebase.view_other_bid'):
        form = UserForm()
    return render(request, "calendar/base.html", context={'form': form})    
    

class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)                
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
        })        
        return context       
    
class ClientStatusUpdateView(BaseMixin, UpdateView):
    model = EstateClient
    form_class = ClientStatusUpdateForm
    template_name = 'clients/client_status_update.html'
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        client = self.kwargs.get('client', None)
        estate = self.kwargs.get('estate', None)
        queryset = queryset.filter(client=client, estate=estate)
        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") % 
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj
    
class EstateRegisterMixin(ModelFormMixin):
    template_name = 'registers/register_update.html'
    form_class = EstateRegisterForm 
    model = EstateRegister
    _addlist = None   
    def get_initial(self):        
        initial = super(EstateRegisterMixin, self).get_initial()        
        if 'bid' in self.kwargs:                  
            initial['bids'] = [self.kwargs['bid']]
        return initial
    def get_context_data(self, **kwargs):                         
        context = super(EstateRegisterMixin, self).get_context_data(**kwargs)
        context.update({
            'PUBLIC_MEDIA_URL' : PUBLIC_MEDIA_URL,
            'next_url': safe_next_link(self.request.get_full_path()),
            'addlist' : self._addlist,
        })
        return context
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')         
        if '_continue' in self.request.POST:                  
            return '%s?%s' % (reverse('register_update', args=[self.object.id]), safe_next_link(next_url)) 
        return next_url
    def form_valid(self, form):
        self.object = form.save(commit=False)        
        self.object.history = prepare_history(self.object.history, self.request.user.pk)        
        return super(EstateRegisterMixin, self).form_valid(form)

class EstateRegisterCreateView(EstateRegisterMixin, CreateView):
    def get_initial(self):        
        initial = super(EstateRegisterCreateView, self).get_initial()
        rtype = self.request.REQUEST.get('type', None)
        if rtype == 'empty':
            initial['name'] = u'Ручная'
        elif rtype == 'based':
            initial['name'] = u'По заявке [%s]' % self.kwargs['bid']
            bid = Bid.objects.get(pk=self.kwargs['bid'])
            fltr = bid.cleaned_filter            
            if fltr:            
                pickle_form = BidPicleForm()
                f = pickle_form.make_filter(fltr)                
                q = Estate.objects
                q = set_estate_filter(q, f, True)                
                estates = list(q.values_list('id', flat=True))
                estates.extend(bid.estates.values_list('id', flat=True))
                initial['estates'] = estates 
                self._addlist = initial['estates']                
        return initial     

class EstateRegisterUpdateView(EstateRegisterMixin, UpdateView):
    pass

class EstateRegisterDeleteView(DeleteMixin, EstateRegisterMixin, DeleteView):
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(EstateRegisterDeleteView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Удаление подборки...',
            'dialig_body'  : u'Подтвердите удаление подборки: %s' % self.object,
        })
        return context
    
class EstateRegisterDetailView(EstateRegisterMixin, DetailView):
    template_name = 'registers/register_detail.html'
    def get_context_data(self, **kwargs):
        context = super(EstateRegisterDetailView, self).get_context_data(**kwargs)        
        estate_list = self.object.estates.all()  
        order_by = self.request.fields
        if order_by:      
            estate_list = estate_list.order_by(','.join(order_by))        
        paginator = Paginator(estate_list, 25)    
        page = self.request.GET.get('page')
        try:
            estates = paginator.page(page)
        except PageNotAnInteger:        
            estates = paginator.page(1)
        except EmptyPage:        
            estates = paginator.page(paginator.num_pages)        
        context.update({
                'paginator': paginator,
                'page_obj': estates,
                'is_paginated': estates.has_other_pages(),
                'object_list': estates.object_list
            })  
        return context  

class AddEstateToRegisterView(BaseUpdateView):   
    model = EstateRegister    
    def action(self, register, estate_pk):                
        register.estates.add(estate_pk)        
    def get(self, request, *args, **kwargs):
        register = self.model.objects.get(pk=self.kwargs['pk'])         
        self.action(register, self.kwargs['estate_pk'])              
        return JsonResponse({'result':'success'})

class RemoveEstateFromRegisterView(AddEstateToRegisterView):
    def action(self, register, estate_pk):                
        register.estates.remove(estate_pk)
    def get(self, request, *args, **kwargs):
        register = self.model.objects.get(pk=self.kwargs['pk'])         
        self.action(register, self.kwargs['estate_pk'])              
        return JsonResponse({'result':'success'})
        
class  EstateRegisterListView(ListView):
    context_object_name = 'register_list'
    template_name = 'registers/register_list.html'    
    paginate_by = 20   
    filtered = False
    def get_queryset(self):        
        q = EstateRegister.objects.select_related()       
        search_form = EstateRegisterFilterForm(self.request.GET)
        filter_dict = search_form.get_filter()
        if filter_dict:
            self.filtered = True                                        
        if len(filter_dict):
            q = q.filter(**filter_dict)
        order_by = self.request.fields
        if order_by:      
            q = q.order_by(','.join(order_by))    
        return q
    def get_context_data(self, **kwargs):
        context = super(EstateRegisterListView, self).get_context_data(**kwargs)
        register_filter_form = EstateRegisterFilterForm(self.request.GET)                                                                    
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'bid_count': Bid.objects.count(),
            'register_filter_form': register_filter_form,
            'filtered': self.filtered,
        })        
        return context

class EstateRegisterSelectView(EstateRegisterListView):
    template_name = 'registers/register_select.html'                
    def get_context_data(self, **kwargs):         
        context = super(EstateRegisterSelectView, self).get_context_data(**kwargs)                    
        context.update ({            
            'bid_pk' : self.kwargs['bid_pk'],
        })        
        return context
    def get_queryset(self):
        q = super(EstateRegisterSelectView, self).get_queryset()
        q = q.exclude(bids__id=self.kwargs['bid_pk'])
        return q

class EstateRegisterBindView(EstateRegisterListView):
    template_name = 'registers/register_bind_estate.html'                
    def get_context_data(self, **kwargs):         
        context = super(EstateRegisterBindView, self).get_context_data(**kwargs)                    
        context.update ({            
            'estate' : Estate.objects.get(pk=self.kwargs['estate']),
        })        
        return context
    def get_queryset(self):
        q = super(EstateRegisterBindView, self).get_queryset()
        return q

class AddRegisterToBid(DetailView):   
    model = EstateRegister
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(AddRegisterToBid, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Привязка...',
            'dialig_body'  : u'Привязать подборку %s к заявке [%s]?' % (self.kwargs['bid_pk'], self.object),
        })
        return context
    def action(self, register, bid_pk):                
        register.bids.add(bid_pk)        
    def post(self, request, *args, **kwargs):
        register = self.model.objects.get(pk=self.kwargs['pk'])         
        self.action(register, self.kwargs['bid_pk'])              
        return HttpResponseRedirect(self.request.REQUEST.get('next', ''))

class RemoveRegisterFromBid(AddRegisterToBid):   
    def get_context_data(self, **kwargs):
        context = super(RemoveRegisterFromBid, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Отвязка...',
            'dialig_body'  : u'Отвязать подборку %s от заявки [%s]?' % (self.kwargs['bid_pk'], self.object),
        })
        return context
    def action(self, register, bid_pk):                
        register.bids.remove(bid_pk) 

class RegisterReportView(EstateRegisterMixin, DetailView):
    def get_context_data(self, **kwargs):
        prefetch_list = ('beside', 'estate_category' , 'contact' , 'bidgs__wall_construcion', 'history',
                                                           'clients__contacts', 'bidgs__estate_type__estate_type_category',
                                                           'stead__estate_type__estate_type_category',
                                                           'bidgs__documents', 'bidgs__levels__layout_set',
                                                           'bidgs__exterior_finish', 'bidgs__roof', 'bidgs__window_type', 'bidgs__heating',
                                                           'bidgs__levels__level_name', 'bidgs__levels__layout_set__furniture',
                                                           'bidgs__levels__layout_set__interior', 'bidgs__levels__layout_set__layout_feature',
                                                           'bidgs__levels__layout_set__layout_type', 'estate_status', 'origin',
                                                           'region', 'locality')
        context = super(RegisterReportView, self).get_context_data(**kwargs)      
        show_outdated = self.request.REQUEST.get('outdated', None)
        if show_outdated:
            estate_list = self.object.estates.prefetch_related(*prefetch_list)
        else:           
            estate_list = self.object.correct_estates.prefetch_related(*prefetch_list)        
        order_by = self.request.fields
        if order_by:      
            estate_list = estate_list.order_by(','.join(order_by))       
        context.update({
                'estate_list': estate_list
            })  
        return context
    
class RestoreFromTrashView(BaseUpdateView):   
    def action(self):                
        self.object.deleted = False        
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.action() 
        self.object.save()             
        return HttpResponseRedirect(reverse('client_detail', args=[self.object.pk]))    

class RestoreClientView(RestoreFromTrashView):
    def get_queryset(self):
        return Client.all_objects.filter(deleted=True)

class BidEventMixin(ModelFormMixin):
    template_name = 'bid/bid_event_update.html'
    form_class = BidEventForm 
    model = BidEvent   
    def get_context_data(self, **kwargs):                         
        context = super(BidEventMixin, self).get_context_data(**kwargs)
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
        })
        return context
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')         
        if '_continue' in self.request.POST:                  
            return '%s?%s' % (reverse('bid_event_update', args=[self.object.id]), safe_next_link(next_url)) 
        return next_url
    def form_valid(self, form):
        self.object = form.save(commit=False)        
        self.object._user_id = self.request.user.pk        
        return super(BidEventMixin, self).form_valid(form)    
    
class BidEventCreateView(BidEventMixin, CreateView):
    def get_initial(self):        
        initial = super(BidEventCreateView, self).get_initial()
        initial['bid'] = self.kwargs['bid']
        initial['date'] = datetime.now()
        
        return initial

class BidEventUpdateView(BidEventMixin, UpdateView):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(BidEventUpdateView, self).dispatch(*args, **kwargs)

class BidEventDeleteView(BidEventMixin, DeleteView):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(BidEventDeleteView, self).dispatch(*args, **kwargs)
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(BidEventDeleteView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Удаление события...',
            'dialig_body'  : u'Подтвердите удаление события: %s' % self.object,
        })
        return context   

class MultiBindEstateToRegister(ModelFormMixin, ProcessFormView):   
    def get(self, request, *args, **kwargs):
        next_url = self.request.GET.get('next', None)
        url_parts = urlparse.urlparse(smart_str(next_url))
        q = EstateRegister.objects.all()      
        search_form = EstateRegisterFilterForm(QueryDict(url_parts[4]))        
        filter_dict = search_form.get_filter()
        if len(filter_dict):
            q = q.filter(**filter_dict)
        if int(self.kwargs['action']) == 0:    
            q = q .filter(estates__id = self.kwargs['estate'])
            for r in q:
                if r.estates.filter(pk=self.kwargs['estate']):         
                    r.estates.remove(self.kwargs['estate'])
        else:
            q = q .exclude(estates__id = self.kwargs['estate'])
            for r in q:
                if not r.estates.filter(pk=self.kwargs['estate']):                                                
                    r.estates.add(self.kwargs['estate'])            
        return HttpResponseRedirect(self.request.GET.get('next', None))
    @user_passes_test(lambda u: u.is_superuser)
    def dispatch(self, *args, **kwargs):
        return super(MultiBindEstateToRegister, self).dispatch(*args, **kwargs)
    
class WordpressQueue(TemplateView):
    template_name = 'wp/wordpress_queue.html'
    def post(self, request, *args, **kwargs):
        error_to_queue = self.request.POST.get('error_to_queue', None)
        if error_to_queue == 'True':
            error_qs = Estate.objects.filter(wp_meta__status=EstateWordpressMeta.ERROR)
            for estate in error_qs:
                estate.wp_meta.status = EstateWordpressMeta.XMLRPC
                estate.wp_meta.save()
        return HttpResponseRedirect(reverse('wordpress_queue'))
    def get_context_data(self, **kwargs):
        context = super(WordpressQueue, self).get_context_data(**kwargs)
        meta_report = self.request.GET.get('meta_report', None)
        if meta_report:
            meta_titles = {
                           'meta_localities': u'Населённые пункты',
                           'meta_estate_types': u'Виды недвижимости',
                           'meta_regions': u'Районы',
                           'meta_statuses': u'Статусы',
                           }
            meta_querysets = {}
            meta_localities = []
            for tax in WordpressTaxonomyTree.objects.exclude(wp_meta_locality=None):  # @UndefinedVariable
                meta_localities.append(tax.wp_meta_locality)
            meta_querysets['meta_localities'] = meta_localities
            meta_querysets['meta_estate_types'] = WordpressMetaEstateType.objects.all()                
            meta_querysets['meta_regions'] = WordpressMetaRegion.objects.all()
            meta_querysets['meta_statuses'] = WordpressMetaStatus.objects.all()
            context.update({
                'meta_queryset' : meta_querysets[meta_report],
                'meta_title' : meta_titles[meta_report],                       
            })                        
        context.update({
            'queue' : Estate.objects.filter(wp_meta__status__in=[EstateWordpressMeta.XMLRPC,EstateWordpressMeta.UNKNOWN], validity=Estate.VALID),
            'err_queue' : Estate.objects.filter(wp_meta__status=EstateWordpressMeta.ERROR),
        })
        return context     


class ClientUpdateBidView(DetailView):   
    model = Client
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(ClientUpdateBidView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Привязка...',
            'dialig_body'  : u'Привязать заказчика %s к заявке [%s]?' % (self.object, self.kwargs['bid_pk']),
        })
        return context
    def update_object(self, client_pk, bid_pk):
        '''
        Вынесена для переопределения в потомках класса
        '''        
        BidClient.objects.create(client_id=client_pk, bid_id=bid_pk)                
    def post(self, request, *args, **kwargs):       
        self.update_object(self.kwargs['pk'], self.kwargs['bid_pk'])       
        #Обновление истории и контакта у заявки                            
        prepare_history(Bid.objects.get(pk=self.kwargs['bid_pk']).history, self.request.user.pk)      
        return HttpResponseRedirect(self.request.REQUEST.get('next', ''))    

class ClientPartnerRemoveView(ClientUpdateBidView):    
    def get_context_data(self, **kwargs):
        context = super(ClientPartnerRemoveView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Отвязка...',
            'dialig_body'  : u'Отвязать заказчика %s от заявки [%s]?' % (self.object, self.kwargs['bid_pk']),
        })
        return context 
    def update_object(self, client_pk, bid_pk):
        bid = Bid.objects.get(pk=bid_pk)
        if bid.client_id == int(client_pk):
            bid.client = None
            bid.save()                 
        BidClient.objects.get(bid_id=bid_pk, client_id=client_pk).delete()   

@user_passes_test(lambda u: u.is_staff)
def estate_list_contacts(request, contact_type_pk):            
    q = Estate.objects.all()        
    filter_form = EstateFilterForm(request.GET)
    filter_dict = filter_form.get_filter()                               
    q = set_estate_filter(q, filter_dict, user=request.user)
    estate_ids = q.values_list('id',flat=True) 
    contacts = Contact.objects.filter(client__estates__id__in=estate_ids, contact_type_id=contact_type_pk, contact_state_id=Contact.AVAILABLE)
    return contacts_csv_response(contacts, contact_type_pk)

@user_passes_test(lambda u: u.is_staff)
def client_list_contacts(request, contact_type_pk):
    q = Client.objects.all()
    search_form = ClientFilterForm(request.GET)
    filter_dict = search_form.get_filter()    
    if len(filter_dict):
        q = q.filter(**filter_dict)       
    client_ids = q.values_list('id',flat=True) 
    contacts = Contact.objects.filter(client_id__in=client_ids, contact_type_id=contact_type_pk, contact_state_id=Contact.AVAILABLE)
    return contacts_csv_response(contacts, contact_type_pk)

@user_passes_test(lambda u: u.is_staff)
def incorrect_contacts(request):     
    contacts = Contact.objects.filter(contact_type_id=Contact.PHONE)
    response = HttpResponse(content_type='text/csv')    
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % 'incorrect_contacts'
    writer = unicodecsv.writer(response)
    writer.writerow(['contact','contact_id','client_id'])
    for contact in contacts:
        if contact.contact[0] != '8' or len(contact.contact) < 9:
            writer.writerow([contact.contact,contact.id,contact.client_id])
    return response

@user_passes_test(lambda u: u.is_staff)
def bid_list_contacts(request, contact_type_pk):            
    q = Bid.objects.all()          
    search_form = BidFilterForm(request.GET)
    filter_dict = search_form.get_filter()    
    geo_list = request.user.userprofile.geo_groups.values_list('id', flat=True)                            
    q = q.filter(geo_groups__id__in=geo_list)
    if len(filter_dict):
        if 'Q' in filter_dict:
            q = q.filter(filter_dict.pop('Q'))                
        q = q.filter(**filter_dict)    
    bid_ids = set(q.values_list('id',flat=True))    
    contacts = Contact.objects.filter(client__bids__id__in=bid_ids, contact_type_id=contact_type_pk, contact_state_id=Contact.AVAILABLE)    
    return contacts_csv_response(contacts, contact_type_pk)

def contacts_csv_response(contacts, contact_type_pk):
    contact_type_id = int(contact_type_pk)
    contact_types = {Contact.EMAIL : 'emails', Contact.PHONE: 'phones'}        
    response = HttpResponse(content_type='text/csv')    
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % contact_types[contact_type_id]
    writer = unicodecsv.writer(response)
    unique_contacts = set(contacts)
    for contact in unique_contacts:
        contact_str = contact.contact 
        if contact_type_id == Contact.PHONE:
            contact_str = format_phone(contact_str)           
        writer.writerow([contact_str,])
    return response

def set_bid_basic_client(request, client_pk, bid_pk):             
    next_url = request.REQUEST.get('next', '')
    bid = Bid.objects.get(pk=bid_pk)
    bid.client_id = client_pk
    bid.save()            
    return HttpResponseRedirect(next_url)

class ManageM2M(View):
    formset = None       
    reverse_name = None   
    template = None 
    instance_model = None       
    def dispatch(self, *args, **kwargs):
        self.instance = get_object_or_404(self.instance_model, pk=kwargs['pk'])
        return super(ManageM2M, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):                 
        formset = self.formset(self.request.POST, instance=self.instance)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
            formset.save()                             
            return HttpResponseRedirect(self.get_success_url())        
        context = self.get_context(request)
        context['formset'] = formset
        return render(request, self.template, context)
    
    def get(self, request, *args, **kwargs):        
        formset = self.formset(instance=self.instance, initial=[self.get_initial()])
        context = self.get_context(request)
        context['formset'] = formset
        return render(request, self.template, context)
    
    def get_context(self, request):
        context = {               
               'next_url': self.get_success_url(),
               'dialig_title': self.get_dialig_title(), 
               }     
        return context
                    
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')                  
        if '_continue' in self.request.POST:                  
            return '%s?%s' % (reverse(self.reverse_name, args=[self.instance.id]), safe_next_link(next_url))
        return next_url
    
    def get_initial(self):
        return {}

class ManageEstateM2M(ManageM2M):          
    template = "estate_dialog/manage_m2m_estate.html"
    instance_model = Estate

class ManageEstateM2MEntrance(ManageEstateM2M):    
    formset = EntranceEstateFormSet       
    reverse_name = "manage_entrances"
    def get_dialig_title(self):
        return u'Виды и выходы для "%s"' % self.instance    

class ManageEstateM2MLinks(ManageM2M):
    template = "estate_dialog/manage_m2m_estate.html"
    formset = GenericLinkFormset       
    reverse_name = "manage_links"
    def dispatch(self, *args, **kwargs):         
        self.model_key = kwargs['model_key']  
        self.instance = get_files_content_object(self.model_key, kwargs['object_pk'])     
        return super(ManageM2M, self).dispatch(*args, **kwargs)
    def get_dialig_title(self):
        return u'Ссылки для "%s"' % self.instance
    def get(self, request, *args, **kwargs):        
        formset = self.formset(instance = self.instance)
        context = self.get_context(request)
        context['formset'] = formset
        return render(request, self.template, context)
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')                  
        if '_continue' in self.request.POST:                  
            return '%s?%s' % (reverse(self.reverse_name, args=[self.model_key, self.instance.id]), safe_next_link(next_url))
        return next_url

def global_search(request):    
    q = request.GET.get('q') 
    pk = re.sub(r'\D', '', q)   
    contact_str = re.sub(r'\s', '', q)
    result = {
                'estates': [],
                'contacts': [],
                'bids': [], 
                'query': q, 
                'not_found': True,                
             }       
    if pk:
        estates = Estate.objects.filter(pk=pk)
        for estate in estates:
            result['estates'].append(estate)
            result['not_found'] = False
        bids = Bid.objects.filter(pk=pk)
        for bid in bids:
            result['bids'].append(bid)
            result['not_found'] = False
        
    if contact_str:      
        contacts = Contact.objects.filter(contact=contact_str)
        for contact in contacts:
            result['contacts'].append(contact)
            result['not_found'] = False
    result['next_url'] = request.REQUEST.get('next', '')
    result['pk'] = pk    
    result['contact_str'] = contact_str    
    return render(request, 'globalsearch/result.html', result)

def csrf_failure(request, reason=""):
    if request.user.is_authenticated:
        next_url = request.REQUEST.get('next', '')
        if not next_url:
            next_url = LOGIN_REDIRECT_URL       
        return redirect(next_url)
    return HttpResponseForbidden()


class BidReportView(BidListView):
    paginate_by = 100
    template_name = 'reports/bid/base.html'
    

    
