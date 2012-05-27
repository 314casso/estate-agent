from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from estatebase.views import EstateTypeView, EstateCreateView, EstateListView, EstateUpdateView,\
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,\
    ContactHistoryListView
from django.contrib.auth.decorators import login_required



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'realestate.views.home', name='home'),
    # url(r'^realestate/', include('realestate.foo.urls')),    
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cat/$', EstateTypeView.as_view(), name='estate_list'),
    url (r'^create/(?P<estate_type>\d+)$', view=EstateCreateView.as_view(), name='estate_create'),
    url (r'^update/(?P<pk>\d+)$', view=EstateUpdateView.as_view(), name='estate_update'),
    url(r'^estatelist/$',EstateListView.as_view(), name='estate_table'),
    url(r'^selectable/', include('selectable.urls')),    
    url(r'^clients/$',ClientListView.as_view(), name='client_list'),
    url (r'^createclient/$', view=login_required(ClientCreateView.as_view()), name='client_create'),
    url (r'^updateclient/(?P<pk>\d+)$', view=ClientUpdateView.as_view(), name='client_update'),
    url (r'^deleteclient/(?P<pk>\d+)$', view=ClientDeleteView.as_view(), name='client_delete'),    
)

urlpatterns += patterns('',
    url (r'^contacthistory/(?P<pk>\d+)/$', ContactHistoryListView.as_view(), name='contact_history' ),        
)
       
