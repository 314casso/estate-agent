from django.views.generic import TemplateView
from models import EstateTypeCategory
from django.views.generic.edit import CreateView
from estatebase.forms import EstateForm
from estatebase.models import EstateType
from django.core.urlresolvers import reverse
from estatebase.models import Estate
from estatebase.tables import EstateTable
from django.shortcuts import render
from django_tables2.config import RequestConfig

class EstateTypeView(TemplateView):    
    template_name = 'index.html'    
    def get_context_data(self, **kwargs):
        context = super(EstateTypeView, self).get_context_data(**kwargs)
        #estate_categories = EstateTypeCategory.objects.all().order_by('name')        
        estate_categories = EstateTypeCategory.objects.all()
        context.update({
            'title': 'base',
            'estate_categories': estate_categories
        })
        return context 
    
class EstateMixin(object):
    model = Estate
    form_class = EstateForm
    def get_success_url(self):
        return reverse('estate_list')        

class EstateCreateView(EstateMixin, CreateView):
    def get_initial(self):        
        initial = super(EstateCreateView, self).get_initial()        
        initial = initial.copy()        
        initial['estate_type'] = self.kwargs['estate_type']
        return initial
    def get_context_data(self, **kwargs):
        context = super(EstateCreateView, self).get_context_data(**kwargs)        
        context.update({
            'estate_type_name': EstateType.objects.get(pk=self.kwargs['estate_type']),            
        })
        return context

#TODO: Convert to ClassBased
def estate_list_view(request):
    table = EstateTable(Estate.objects.all().select_related())
    RequestConfig(request, paginate={"per_page": 5}).configure(table)
    context = {
            'table': table,
            'title': 'list'
        }
    return render(request, 'estate_list.html', context)