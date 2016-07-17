# Create your views here.
from django.views.generic.list import ListView
from exportdata.models import ContentTypeMapper, ValueMapper, MappedNode
from django.views.generic.detail import DetailView
from django.contrib.contenttypes.models import ContentType
import simplejson as json
from django.http import HttpResponse
from django.db import transaction


class FeedContentTypeListView(ListView):
    model = ContentTypeMapper
    
class FeedContentTypeDetailView(DetailView):
    model = ContentTypeMapper
    def get_context_data(self, **kwargs):
        context = super(FeedContentTypeDetailView, self).get_context_data(**kwargs)
        items = []        
        mapped_node = self.kwargs.get('mapped_node')
        print self.request
        for obj in self.object.content_type.model_class().objects.all().order_by('name'):
            content_type = ContentType.objects.get_for_model(obj)
            obj.content_type = content_type
            try:
                obj.value_mapper = ValueMapper.objects.get(content_type__pk=content_type.id, object_id=obj.id, mapped_node__pk=mapped_node)
            except ValueMapper.DoesNotExist:
                pass                                                            
            items.append(obj)         
        context.update({
            'items' : items,        
            'mapped_node' : MappedNode.objects.get(pk=mapped_node),
        })
        return context    

@transaction.commit_on_success    
def save_data(request):    
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':            
            try:
                items = json.loads(request.body)                
                for item in items.itervalues():
                    object_id = item.get('object')
                    content_type_id = item.get('contenttype')                   
                    mapped_node_id = item.get('mappednode')
                    q = ValueMapper.objects.filter(content_type_id=content_type_id, object_id=object_id, mapped_node_id=mapped_node_id)
                    value_mapper = q[0] if q else None                        
                    xmlvalue = item.get('xmlvalue')
                    if value_mapper:                                            
                        if xmlvalue:                            
                            value_mapper.xml_value = xmlvalue 
                            value_mapper.save()
                        else:
                            value_mapper.delete()
                    elif item.get('xmlvalue'):                       
                        ValueMapper.objects.create(content_type_id=content_type_id, object_id=object_id, mapped_node_id=mapped_node_id, xml_value=item.get('xmlvalue'))                            
                response_data['result'] = 1
            except Exception, e:          
                response_data['error'] = str(e)
                response_data['result'] = 0
                if transaction.is_dirty():
                    transaction.rollback()                    
    response_json = json.dumps(response_data)                   
    return HttpResponse(response_json, content_type="application/json")    