# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from devrep.models import Partner, WorkType, ClientPartner
from django.views.generic.edit import CreateView, ModelFormMixin, DeleteView,\
    UpdateView
from estatebase.helpers.functions import safe_next_link
from devrep.forms import PartnerForm
from django.views.generic.detail import DetailView
from estatebase.views import DeleteMixin, ClientListView
from estatebase.models import prepare_history, Client
from django.http import HttpResponseRedirect
from estatebase.forms import ClientFilterForm

class PartnerListView(ListView):    
    filtered = False
    template_name = 'partner_list.html'
    paginate_by = 7      
    def get_queryset(self):        
        q = Partner.objects.all()        
        #filter_form = self.filter_form(self.request.GET)
        #filter_dict = filter_form.get_filter()        
        #if filter_dict:
        #    self.filtered = True                    
        #q = set_estate_filter(q, filter_dict, user=self.request.user)
        #order_by = self.request.fields 
        #if order_by:      
        #    return q.order_by(','.join(order_by))
        return q
    def get_context_data(self, **kwargs):
        context = super(PartnerListView, self).get_context_data(**kwargs)
#         filter_form = self.filter_form(self.request.GET)
#         
        params = self.request.GET.copy()      
        get_params = params.urlencode()
                   
        context.update({            
            'next_url': safe_next_link(self.request.get_full_path()),
            'total_count': WorkType.objects.count(),
            'filter_count' : self.get_queryset().count(),
#             'filter_form': filter_form,
#             'filter_action': '%s?next=%s' % (reverse('estate-list'), self.request.GET.get('next','')),
            'filtered' :self.filtered,
            'get_params': get_params,
        })        
        return context
    

class PartnerMixin(ModelFormMixin):    
    form_class = PartnerForm
    template_name = 'partner_form.html'
    model = Partner 
    def form_valid(self, form):
        self.object = form.save(commit=False)        
        self.object._user_id = self.request.user.pk        
        return super(PartnerMixin, self).form_valid(form)   
        
class PartnerCreateView(PartnerMixin, CreateView): 
    def get_context_data(self, **kwargs):
        context = super(PartnerCreateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Добавление нового партнера'
        })        
        return context    

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
