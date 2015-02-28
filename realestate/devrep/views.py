# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from devrep.models import Partner, WorkType
from django.views.generic.edit import CreateView, ModelFormMixin
from estatebase.helpers.functions import safe_next_link

class PartnerListView(ListView):    
    filtered = False
    template_name = 'partner_list.html'
    paginate_by = 7      
    def get_queryset(self):        
        q = WorkType.objects.all()        
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
    model = Partner
    template_name = 'partner_form.html'
    
    
class PartnerCreateView(PartnerMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super(PartnerCreateView, self).get_context_data(**kwargs)
        context.update({
            'dialig_title' : u'Добавление нового партнера'
        })        
        return context    
    