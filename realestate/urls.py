from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from estatebase.views import EstateTypeView, EstateListView, BidgCreateView,\
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,\
    ContactHistoryListView, ContactUpdateView, BidgUpdateView, ClientSelectView,\
    ClientUpdateEstateView, ClientRemoveEstateView, BidgDetailView
from django.contrib.auth.decorators import login_required




admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'realestate.views.home', name='home'),
    # url(r'^realestate/', include('realestate.foo.urls')),    
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cat/$', EstateTypeView.as_view(), name='estate_list'),        
    url(r'^estatelist/$',EstateListView.as_view(), name='estate_table'),
    url(r'^selectable/', include('selectable.urls')),    
    url(r'^clients/$',ClientListView.as_view(), name='client_list'),
    url(r'^clients/(?P<estate_pk>\d+)$',ClientSelectView.as_view(), name='client_select'),
    url (r'^clientcreate/$', view=login_required(ClientCreateView.as_view()), name='client_create'),
    url (r'^clientupdate/(?P<pk>\d+)$', view=ClientUpdateView.as_view(), name='client_update'),
    url (r'^clientdelete/(?P<pk>\d+)$', view=ClientDeleteView.as_view(), name='client_delete'),    
)

urlpatterns += patterns('',
    url (r'^contacthistory/(?P<pk>\d+)/$', ContactHistoryListView.as_view(), name='contact_history' ),        
    url (r'^contactupdate/(?P<pk>\d+)/$', ContactUpdateView.as_view(), name='contact_update' ),
)
 
urlpatterns += patterns('',
    url (r'^clientestate/(?P<pk>\d+)/(?P<estate_pk>\d+)$', ClientUpdateEstateView.as_view(), name='client_estate'),   
    url (r'^clientestateunbind/(?P<pk>\d+)/(?P<estate_pk>\d+)$', ClientRemoveEstateView.as_view(), name='client_estate_unbind'),     
) 
       
urlpatterns += patterns('',
    url (r'^bidgcreate/(?P<estate_type>\d+)$', view=BidgCreateView.as_view(), name='bidg_create'),
    url (r'^bidgupdate/(?P<pk>\d+)$', view=BidgUpdateView.as_view(), name='bidg_update'),
    url (r'^bidgdetail/(?P<pk>\d+)$', view=BidgDetailView.as_view(), name='bidg_detail'),
)

