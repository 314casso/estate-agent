from django.conf.urls.defaults import patterns, include, url
from estatebase.views import EstateTypeView, EstateListView,\
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,\
    ContactHistoryListView, ContactUpdateView, ClientSelectView,\
    ClientUpdateEstateView, ClientRemoveEstateView, \
    EstateCreateView, ApartmentDetailView,\
    EstateCommunicationUpdateView,\
    EstateParamUpdateView, EstateUpdateView, ApartmentCreateView,\
    ApartmentUpdateView, LevelCreateView, LevelUpdateView, LevelDeleteView,\
    upload_images

urlpatterns = patterns('',    
    url(r'^cat/$', EstateTypeView.as_view(), name='estate_list'),        
    url(r'^estatelist/$',EstateListView.as_view(), name='estate_list'),
    url(r'^selectable/', include('selectable.urls')),    
    url(r'^clients/$',ClientListView.as_view(), name='client_list'),
    url(r'^clients/(?P<estate_pk>\d+)$',ClientSelectView.as_view(), name='client_select'),
    url (r'^clientcreate/$', view=ClientCreateView.as_view(), name='client_create'),
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
    url (r'^estatecreate/(?P<estate_type>\d+)$', view=EstateCreateView.as_view(), name='estate_create'),
    url (r'^estateupdate/(?P<pk>\d+)$', view=EstateUpdateView.as_view(), name='estate_update'),        
    url (r'^estatecommupdate/(?P<pk>\d+)$', view=EstateCommunicationUpdateView.as_view(), name='estate_comm_update'),    
    url (r'^estateparamsupdate/(?P<pk>\d+)$', view=EstateParamUpdateView.as_view(), name='estate_params_update'),
)

urlpatterns += patterns('',
    url (r'^apartmentdetail/(?P<pk>\d+)$', view=ApartmentDetailView.as_view(), name='apartment_detail'),
    url (r'^apartmentcreate/(?P<estate>\d+)$', view=ApartmentCreateView.as_view(), name='apartment_create'),
    url (r'^apartmentupdate/(?P<pk>\d+)$', view=ApartmentUpdateView.as_view(), name='apartment_update'),
)

urlpatterns += patterns('',
    url (r'^levelcreate/(?P<bidg>\d+)$', view=LevelCreateView.as_view(), name='level_create'),
    url (r'^levelupdate/(?P<pk>\d+)$', view=LevelUpdateView.as_view(), name='level_update'),
    url (r'^leveldelete/(?P<pk>\d+)$', view=LevelDeleteView.as_view(), name='level_delete'),
)   

urlpatterns += patterns('',
    url (r'^uploadimages/$', view=upload_images, name='upload_images'),
)