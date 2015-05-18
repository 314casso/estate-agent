# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from devrep.models import Partner, WorkType, ClientPartner, Gear, DevProfile,\
    ExtraProfile, Quality
from django.views.generic.edit import CreateView, ModelFormMixin, DeleteView,\
    UpdateView
from estatebase.helpers.functions import safe_next_link
from devrep.forms import PartnerForm, ClientPartnerThroughUpdateForm,\
    AddressForm, DevProfileForm, WorkTypeProfileFormSet, ExtraProfileForm,\
    PartnerFilterForm, GoodsProfileM2MFormSet
from django.views.generic.detail import DetailView
from estatebase.views import DeleteMixin, ClientListView, BaseMixin
from estatebase.models import prepare_history, Client
from django.http import HttpResponseRedirect, Http404, HttpResponse
from estatebase.forms import ClientFilterForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import escape, escapejs
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template.context import RequestContext
from django.views.generic.base import View

class PartnerListView(ListView):    
    filtered = False
    template_name = 'partner_list.html'
    paginate_by = 7
    filter_form = PartnerFilterForm
    
    @method_decorator(permission_required('devrep.developer', raise_exception=True))
    def dispatch(self, *args, **kwargs):                
        return super(PartnerListView, self).dispatch(*args, **kwargs)      
    
    def get_queryset(self):        
        q = Partner.objects.all()        
        filter_form = self.filter_form(self.request.GET)
        filter_dict = filter_form.get_filter()             
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
        context = super(PartnerListView, self).get_context_data(**kwargs)
        filter_form = self.filter_form(self.request.GET)
        params = self.request.GET.copy()      
        get_params = params.urlencode()
                   
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'total_count': Partner.objects.count(),
            'filter_count' : self.get_queryset().count(),
            'filter_form': filter_form,            
            'filtered' :self.filtered,
            'get_params': get_params,
        })        
        return context

class PartnerSelectView(PartnerListView):
    template_name = 'partner_select.html'
    def get_client(self):
        return Client.objects.get(pk=self.kwargs['client_pk'])            
    def get_context_data(self, **kwargs):         
        context = super(PartnerSelectView, self).get_context_data(**kwargs)                    
        context.update ({            
            'client' : self.get_client(),
            'filter_form' : self.filter_form(self.request.GET),
        })        
        return context
    def get_queryset(self):
        q = super(PartnerSelectView, self).get_queryset()
        client = self.get_client()
        q = q.exclude(id__in=client.clientpartner_set.all().values_list('partner_id', flat=True))        
        return q

class PartnerMixin(ModelFormMixin):    
    form_class = PartnerForm
    template_name = 'partner_form.html'
    model = Partner 
    
    @method_decorator(permission_required('devrep.developer', raise_exception=True))
    def dispatch(self, *args, **kwargs):                
        return super(PartnerMixin, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        context = self.get_context_data()
        address_form = context['address_form']
        if address_form.is_valid():
            address = address_form.save()             
            self.object = form.save(commit=False)        
            self.object._user_id = self.request.user.pk
            self.object.address = address                
            return super(PartnerMixin, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, address_form=address_form))
    
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')         
        if '_continue' in self.request.POST:                  
            return '%s?%s' % (reverse('partner_update', args=[self.object.id]), safe_next_link(next_url)) 
        return next_url
            
    def get_context_data(self, **kwargs):
        context = super(PartnerMixin, self).get_context_data(**kwargs)
        address = self.object.address if self.object else None
        if self.request.POST:
            if not 'address_form' in context:                  
                context['address_form'] = AddressForm(self.request.POST, instance=address)
        else:
            context['address_form'] = AddressForm(instance=address)
        context.update({
            'dialig_title' : u'Добавление нового партнера',            
        })    
        return context
    
        
class PartnerCreateView(PartnerMixin, CreateView): 
    pass    


class PartnerUpdateView(PartnerMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super(PartnerUpdateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Редактирование портнера [%s] «%s»' % (self.object.pk, self.object) 
        })        
        return context


class PartnerDetailView(PartnerMixin, DetailView):    
    template_name = 'partner_detail.html'
    def get_context_data(self, **kwargs):
        context = super(PartnerDetailView, self).get_context_data(**kwargs)                
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
        })        
        return context  
    
    
class PartnerDeleteView(DeleteMixin, PartnerMixin, DeleteView):
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(PartnerDeleteView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Удаление партнера...',
            'dialig_body'  : u'Подтвердите удаление партнера: %s' % self.object,
        })
        return context


class ClientPartnerSelectView(ClientListView):
    template_name = 'client_partner_select.html'
    def get_bid(self):
        bid = Partner.objects.get(pk=self.kwargs['partner_pk'])
        return bid            
    def get_context_data(self, **kwargs):         
        context = super(ClientPartnerSelectView, self).get_context_data(**kwargs)                    
        context.update ({            
            'partner' : self.get_bid(),
            'client_filter_form' : ClientFilterForm(self.request.GET),
        })        
        return context
    def get_queryset(self):
        q = super(ClientPartnerSelectView, self).get_queryset()
        q = q.exclude(bids_m2m__id=self.kwargs['partner_pk'])
        return q


class ClientPartnerUpdateView(DetailView):   
    model = Client
    template_name = 'confirm.html'
    PARTNER_CLIENT_STATUS = 1
    def get_context_data(self, **kwargs):
        context = super(ClientPartnerUpdateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Привязка...',
            'dialig_body'  : u'Привязать работника %s к партнеру [%s]?' % (self.object, self.kwargs['partner_pk']),
        })
        return context
    def update_object(self, client_pk, partner_pk):
        ClientPartner.objects.create(client_id=client_pk, partner_id=partner_pk, partner_client_status_id=self.PARTNER_CLIENT_STATUS)                
    def post(self, request, *args, **kwargs):       
        self.update_object(self.kwargs['pk'], self.kwargs['partner_pk'])      
        prepare_history(Partner.objects.get(pk=self.kwargs['partner_pk']).history, self.request.user.pk)     
        return HttpResponseRedirect(self.request.REQUEST.get('next', ''))    


class ClientPartnerRemoveView(ClientPartnerUpdateView):    
    def get_context_data(self, **kwargs):
        context = super(ClientPartnerRemoveView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Отвязка...',
            'dialig_body'  : u'Отвязать работника %s от партнера [%s]?' % (self.object, self.kwargs['partner_pk']),
        })
        return context 
    def update_object(self, client_pk, partner_pk):                         
        ClientPartner.objects.get(partner_id=partner_pk, client_id=client_pk).delete() 


class ClientPartnerThroughUpdateView(BaseMixin, UpdateView):
    model = ClientPartner
    form_class = ClientPartnerThroughUpdateForm
    template_name = 'client_partner_through_update.html'
    def get_object(self, queryset=None):        
        client = self.kwargs.get('client', None)
        partner = self.kwargs.get('partner', None)
        if queryset is None:
            queryset = self.get_queryset()
        queryset =  queryset.filter(client=client, partner=partner)
        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") % 
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class PopupCreateMixin(CreateView):
    title = None
    def get_context_data(self, **kwargs):
        context = super(PopupCreateMixin, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : self.title
        })        
        return context    
    def form_valid(self, form):
        self.object = form.save(commit=True)
        if  '_popup' in self.request.POST:            
            return HttpResponse(
            '<!DOCTYPE html><html><head><title></title></head><body>'
            '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script></body></html>' % \
            (escape(self.object.pk), escapejs(self.object)))                
        return super(PopupCreateMixin, self).form_valid(form)   


class GearCreateView(PopupCreateMixin):
    title = u'Добавление новой техники'
    model = Gear    
    
    
class DevProfileMixin(ModelFormMixin):
    form_class = DevProfileForm
    template_name = 'dev_profile_simple_form.html'
    model = DevProfile
    
    @method_decorator(permission_required('devrep.developer', raise_exception=True))
    def dispatch(self, *args, **kwargs):                
        return super(DevProfileMixin, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object._user_id = self.request.user.pk
        self.object.save()      
        super(DevProfileMixin, self).form_valid(form)
        client_pk = form.cleaned_data.get('client_pk', None)
        if client_pk:   
            client = Client.objects.get(pk=client_pk)
            if not client.dev_profile:
                client.dev_profile = self.object
                client.save() 
        return super(DevProfileMixin, self).form_valid(form)
    def get_context_data(self, **kwargs):                         
        context = super(DevProfileMixin, self).get_context_data(**kwargs)                       
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'dialig_title': u'Строительный профиль',    
        })
        return context
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')                  
        if '_continue' in self.request.POST:                  
            return '%s?%s' % (reverse('dev_profile_update', args=[self.object.id]), safe_next_link(next_url))
        return next_url


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

class ManageDevProfileM2M(ManageM2M):          
    template = "manage_m2m_dev_profile.html"
    instance_model = DevProfile


class ManageDevProfileM2MWorktype(ManageDevProfileM2M):    
    formset = WorkTypeProfileFormSet       
    reverse_name = "manage_worktype_profile"
    
    def get_dialig_title(self):
        return u'Управление видами работ для "%s"' % self.instance.client
    

class ManageDevProfileM2MGoods(ManageDevProfileM2M):    
    formset = GoodsProfileM2MFormSet       
    reverse_name = "manage_goods_profile"
    def get_dialig_title(self):
        return u'Управление товарами и услугами для "%s"' % self.instance.client  


class DevProfileCreateView(DevProfileMixin, CreateView): 
    def get_initial(self):        
        initial = super(DevProfileCreateView, self).get_initial()
        initial['client_pk'] = int(self.kwargs.get('client_pk'))        
        return initial  
    
    def get_context_data(self, **kwargs):                         
        context = super(DevProfileCreateView, self).get_context_data(**kwargs)                       
        context.update({          
            'dialig_title': u'Добавление строительного профиля',    
        })
        return context     


class DevProfileUpdateView(DevProfileMixin, UpdateView): 
    def get_context_data(self, **kwargs):                         
        context = super(DevProfileUpdateView, self).get_context_data(**kwargs)                       
        context.update({          
            'dialig_title': u'Редактирование строительного профиля для "%s"' % self.object.client,    
        })
        return context


class DevProfileDeleteView(DevProfileMixin, DeleteView):
    template_name = 'confirm.html'
    def get_context_data(self, **kwargs):
        context = super(DevProfileDeleteView, self).get_context_data(**kwargs)        
        context.update({
            'dialig_title' : u'Удаление профиля строителя...',
            'dialig_body'  : u'Подтвердите удаление профиля: %s' % self.object,
        })
        return context
    
    def get_success_url(self):
        return reverse('client-list')        


class DevProfileDetailView(DevProfileMixin, DetailView): 
    template_name = 'dev_profile_detail.html'


class ExtraProfileMixin(ModelFormMixin):
    form_class = ExtraProfileForm
    template_name = 'extra_profile_form.html'
    model = ExtraProfile
    def form_valid(self, form):
        context = self.get_context_data()
        address_form = context['address_form']
        if address_form.is_valid():
            address = address_form.save()
            self.object = form.save(commit=False)     
            self.object.address = address         
            self.object.save()                        
            client_pk = form.cleaned_data.get('client_pk', None)
            if client_pk:        
                client = Client.objects.get(pk=client_pk)
                client.extra_profile = self.object
                client.save() 
            return super(ExtraProfileMixin, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, address_form=address_form))
    def get_context_data(self, **kwargs):                         
        context = super(ExtraProfileMixin, self).get_context_data(**kwargs)                        
        address = self.object.address if self.object else None
        if self.request.POST:
            if not 'address_form' in context:                  
                context['address_form'] = AddressForm(self.request.POST, instance=address)
        else:
            context['address_form'] = AddressForm(instance=address)            
        return context
    def get_success_url(self):   
        next_url = self.request.REQUEST.get('next', '')                  
        if '_continue' in self.request.POST:                  
            return '%s?%s' % (reverse('extra_profile_update', args=[self.object.id]), safe_next_link(next_url))
        return next_url
    
    
class ExtraProfileCreateView(ExtraProfileMixin, CreateView): 
    def get_initial(self):        
        initial = super(ExtraProfileCreateView, self).get_initial()
        initial['client_pk'] = int(self.kwargs.get('client_pk'))        
        return initial


class ExtraProfileUpdateView(ExtraProfileMixin, UpdateView): 
    pass
        