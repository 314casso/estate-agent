# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from models import EstateTypeCategory
from django.views.generic.edit import CreateView, ModelFormMixin, UpdateView, \
    DeleteView 
from estatebase.forms import ClientForm, ContactFormSet, \
    ClientFilterForm, ContactHistoryFormSet, ContactForm, \
    EstateCreateForm, EstateCommunicationForm, \
    EstateParamForm, ApartmentForm, LevelForm, LevelFormSet, ImageUpdateForm, \
    SteadUpdateForm
from estatebase.models import EstateType, Contact, Level, EstatePhoto, \
    prepare_history, Stead
from django.core.urlresolvers import reverse
from estatebase.models import Estate, Client
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from estatebase.models import ExUser, Bidg
from estatebase.helpers.functions import safe_next_link
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

class BaseMixin():
    def get_success_url(self):   
        if '_save' in self.request.POST:     
            return self.request.REQUEST.get('next', '')
        return ''    

class HistoryMixin(BaseMixin, ModelFormMixin):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = ExUser.objects.get(pk=self.request.user.pk) 
        self.object.history = prepare_history(self.object.history, user)        
        return super(HistoryMixin, self).form_valid(form)

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
            estate_photo.save()  
    return HttpResponseRedirect(request.REQUEST.get('next', ''))         


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

class EstateTypeView(TemplateView):    
    template_name = 'index.html'        
    def get_context_data(self, **kwargs):
        context = super(EstateTypeView, self).get_context_data(**kwargs)                
        estate_categories = EstateTypeCategory.objects.all()
        #TODO: пример фильтрации
        #filtered = (x for x in Contact.objects.all() if x.state_css == 'available-state')

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
        estate_categories = EstateType.objects.filter(object_type='BIDG').select_related().order_by('estate_type_category')
        context.update({            
            'estate_categories': estate_categories,
            'estate': self.kwargs['estate']                       
        })        
        return context

class EstateCreateView(HistoryMixin, CreateView):
    template_name = 'estate_create.html'     
    model = Estate   
    form_class = EstateCreateForm
    def get_initial(self):        
        initial = super(EstateCreateView, self).get_initial()                
        initial['estate_type'] = self.kwargs['estate_type']
        return initial
    def get_context_data(self, **kwargs):
        context = super(EstateCreateView, self).get_context_data(**kwargs)        
        context.update({
            'estate_type': EstateType.objects.get(pk=self.kwargs['estate_type']),
            'next_url': safe_next_link(self.request.get_full_path()),
        })        
        return context
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')                                  
        return '%s?%s' % (self.object.detail_link, safe_next_link(next_url))

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
            'margin': '%d (%d%%)' % (r, p),
            'images': self.object.images.all()[:6],                       
        })        
        return context
    
class EstateUpdateView(HistoryMixin, UpdateView):
    model = Estate
    template_name = 'estate_create.html'
    form_class = EstateCreateForm
    def get_context_data(self, **kwargs):
        context = super(EstateUpdateView, self).get_context_data(**kwargs)        
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'estate_type': self.object.estate_type,
        })        
        return context    

class EstateCommunicationUpdateView(EstateUpdateView):
    template_name = 'estate_comm.html'
    form_class = EstateCommunicationForm

class EstateParamUpdateView(EstateUpdateView):    
    template_name = 'estate_params.html'
    form_class = EstateParamForm

class EstateListView(ListView):    
    template_name = 'estate_short_list.html'
    paginate_by = 10
    def get_queryset(self):        
        #q = Estate.objects.all().select_related().prefetch_related('clients__origin','clients__client_type','clients__history','bidgs')
        q = Estate.objects.all().select_related('region','locality','microdistrict','street').prefetch_related('bidgs').filter(clients__address__icontains=u'там')
        return q
    def get_context_data(self, **kwargs):
        context = super(EstateListView, self).get_context_data(**kwargs)        
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'total_count': Estate.objects.count()
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

class ClientUpdateEstateView(DetailView):   
    model = Client
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(ClientUpdateEstateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Привязка...',
            'dialig_body'  : u'Привязать клиента %s к объекту [%s]?' % (self.object, self.kwargs['estate_pk']),
        })
        return context
    def update_object(self):
        '''
        Вынесена для переопределения в потомках класса
        '''        
        self.object.estates.add(self.kwargs['estate_pk'])        
    def post(self, request, *args, **kwargs):        
        self.object = Client.objects.get(pk=self.kwargs['pk'])
        self.update_object()
        user = ExUser.objects.get(pk=self.request.user.pk)                
        self.object.save(user=user)
        #Обновление истории объекта
        estate = Estate.objects.get(pk=self.kwargs['estate_pk'])
        prepare_history(estate.history, user)
        return HttpResponseRedirect(self.request.REQUEST.get('next', ''))    

class ClientRemoveEstateView(ClientUpdateEstateView):    
    def get_context_data(self, **kwargs):
        context = super(ClientRemoveEstateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Отвязка...',
            'dialig_body'  : u'Отвязать клиента %s от объекта [%s]?' % (self.object, self.kwargs['estate_pk']),
        })
        return context 
    def update_object(self):
        self.object.estates.remove(self.kwargs['estate_pk'])            
        
class ObjectMixin(ModelFormMixin):    
    model = Bidg    
    continue_url = None    
    def form_valid(self, form):
        prepare_history(self.get_estate().history, user=ExUser.objects.get(pk=self.request.user.pk))       
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
    form_class = ApartmentForm   
    continue_url = 'apartment_update'
    def get_initial(self):        
        initial = super(ApartmentCreateView, self).get_initial()                
        initial['estate'] = self.kwargs['estate']
        return initial

class ApartmentUpdateView(ObjectMixin, UpdateView):
    template_name = 'bidg_form.html'        
    form_class = ApartmentForm   
    continue_url = 'apartment_update'        

#TODO: Unused!!!
class ApartmentDetailView(EstateDetailView):
    template_name = 'apartment_detail.html'    
    def get_context_data(self, **kwargs):
        context = super(ApartmentDetailView, self).get_context_data(**kwargs)                
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
        })        
        return context

class ClientListView(ListView):
    template_name = 'client_list.html'
    context_object_name = "clients"
    paginate_by = 5    
    def get_queryset(self):                        
        q = Client.objects.all().select_related().prefetch_related('origin','contacts__contact_state','contacts__contact_type')
        search_form = ClientFilterForm(self.request.GET)
        filter_dict = search_form.get_filter()
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
        })        
        return context

class ClientSelectView(ClientListView):
    template_name = 'client_select.html'
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

class ClientMixin(ModelFormMixin):
    template_name = 'client_form.html'
    model = Client
    form_class = ClientForm          
    def form_valid(self, form):
        context = self.get_context_data()
        contact_form = context['contact_formset']
        if contact_form.is_valid():
            self.object = form.save(commit=False)                         
            self.object.save(user=ExUser.objects.get(pk=self.request.user.pk))             
            contact_form.instance = self.object
            contact_form.save()
            return super(ModelFormMixin, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')         
        if '_continue' in self.request.POST:                  
            return '%s?%s' % (reverse('client_update', args=[self.object.id]), safe_next_link(next_url)) 
        return next_url
    def get_context_data(self, **kwargs):
        context = super(ClientMixin, self).get_context_data(**kwargs)                
        if self.request.POST:
            context['contact_formset'] = ContactFormSet(self.request.POST, instance=self.object)            
        else:
            context['contact_formset'] = ContactFormSet(instance=self.object)
        return context                        

class ClientCreateView(ClientMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super(ClientCreateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : 'Добавление нового клиента'
        })        
        return context    
      
class ClientUpdateView(ClientMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : 'Редактирование клиента «%s»' % self.object 
        })        
        return context

class ClientDeleteView(ClientMixin, DeleteView):
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(ClientDeleteView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Удаление клиента...',
            'dialig_body'  : u'Подтвердите удаление клиента: %s' % self.object,
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
    form_class = SteadUpdateForm   
    continue_url = 'stead_update'

class BidgAppendView(TemplateView):    
    template_name = 'confirm.html'    
    def get_context_data(self, **kwargs):        
        context = super(BidgAppendView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Добавление строения...',
            'dialig_body'  : u'Добавить %s к объекту [%s]?' % (self.kwargs['estate_type'], self.kwargs['estate']),
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
    def update_object(self):                        
        bidg = Bidg.objects.get(pk=self.kwargs['pk'])
        self.estate = bidg.estate
        bidg.delete();
    def get_context_data(self, **kwargs):        
        context = super(BidgAppendView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Удаление строения...',
            'dialig_body'  : u'Удалить строение из объекта?'
        })
        return context    
