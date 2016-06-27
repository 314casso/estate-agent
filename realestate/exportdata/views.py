# Create your views here.
from django.views.generic.list import ListView
from exportdata.models import FeedContentType, FeedMapper, BaseFeed
from django.views.generic.detail import DetailView
from django.contrib.contenttypes.models import ContentType
import simplejson as json
from django.http import HttpResponse
from django.db import transaction

class FeedContentTypeListView(ListView):
    model = FeedContentType
    
class FeedContentTypeDetailView(DetailView):
    model = FeedContentType
    def get_context_data(self, **kwargs):
        context = super(FeedContentTypeDetailView, self).get_context_data(**kwargs)
        items = []        
        feed = self.kwargs.get('feed')
        print self.request
        for obj in self.object.content_type.model_class().objects.all().order_by('name'):
            content_type = ContentType.objects.get_for_model(obj)
            obj.content_type = content_type
            try:
                obj.feed_map = FeedMapper.objects.get(content_type__pk=content_type.id, object_id=obj.id, feed__pk=feed)
            except FeedMapper.DoesNotExist:
                pass                                                            
            items.append(obj)         
        context.update({
            'items' : items,        
            'feed' : BaseFeed.objects.get(pk=feed),
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
                    feed = item.get('feed')
                    q = FeedMapper.objects.filter(content_type_id=content_type_id, object_id=object_id, feed_id=feed)
                    feed_mapper = q[0] if q else None                        
                    xmlvalue = item.get('xmlvalue')
                    if feed_mapper:                                            
                        if xmlvalue:                            
                            feed_mapper.xml_value = xmlvalue 
                            feed_mapper.save()
                        else:
                            feed_mapper.delete()
                    elif item.get('xmlvalue'):                       
                        FeedMapper.objects.create(content_type_id=content_type_id, object_id=object_id, feed_id=item.get('feed'), xml_value=item.get('xmlvalue'))                            
                response_data['result'] = 1
            except Exception, e:          
                response_data['error'] = str(e)
                response_data['result'] = 0
                if transaction.is_dirty():
                    transaction.rollback()                    
    response_json = json.dumps(response_data)                   
    return HttpResponse(response_json, content_type="application/json")    