from django.conf.urls.defaults import patterns, url
from exportdata.views import FeedContentTypeListView, FeedContentTypeDetailView, save_data

urlpatterns = patterns('',
    url(r'^typelist/$', FeedContentTypeListView.as_view(), name='type_list'),
    url(r'^typedetail/(?P<pk>\d+)/(?P<mapped_node>\d+)$', FeedContentTypeDetailView.as_view(), name='type_detail'),
    url(r'^savedata$', save_data, name='save_data'),
)