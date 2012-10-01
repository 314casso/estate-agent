from django.conf.urls.defaults import patterns, include, url
from estatebase.views import EstateTypeView, EstateListView, ClientListView, \
    ClientCreateView, ClientUpdateView, ClientDeleteView, ContactHistoryListView, \
    ContactUpdateView, ClientSelectView, ClientUpdateEstateView, \
    ClientRemoveEstateView, EstateCreateView, EstateCommunicationUpdateView, \
    EstateParamUpdateView, EstateUpdateView, ApartmentCreateView, \
    ApartmentUpdateView, LevelCreateView, LevelUpdateView, LevelDeleteView, \
    upload_images, EstateImagesView, SwapEstatePhotoView, ImageUpdateView, \
    ImageDeleteView, EstateDetailView, SteadUpdateView, EstateTypeViewAjax, \
    BidgAppendView, BidgRemoveView, EstateListDetailsView, PlaceableTypeViewAjax,\
    BidCreateView, BidUpdateView, BidListView, BidDeleteView,\
    ClientDetailView, EstateDeleteView, BidDetailView, EstateRegisterCreateView,\
    EstateRegisterUpdateView, EstateRegisterDeleteView, EstateSelectListView,\
    EstateRegisterDetailView, AddEstateToRegisterView,\
    RemoveEstateFromRegisterView, EstateRegisterListView,\
    EstateRegisterSelectView, AddRegisterToBid, RemoveRegisterFromBid,\
    EstateCreateClientView

urlpatterns = patterns('',    
    url(r'^cat/$', EstateTypeView.as_view(), name='estate_list'),        
    url(r'^estatelist/$',EstateListView.as_view(), name='estate_list'),
    url(r'^estateselectlist/(?P<selected>\d+)$',EstateSelectListView.as_view(), name='estate_select_list'),
    url(r'^estatelistdetails/(?P<pk>\d+)$',EstateListDetailsView.as_view(), name='estate_list_details'),
    url(r'^selectable/', include('selectable.urls')),    
    url(r'^clients/$',ClientListView.as_view(), name='client_list'),
    url(r'^clients/(?P<estate_pk>\d+)$',ClientSelectView.as_view(), name='client_select'),
    url (r'^clientcreate/$', view=ClientCreateView.as_view(), name='client_create'),
    url (r'^clientupdate/(?P<pk>\d+)$', view=ClientUpdateView.as_view(), name='client_update'),
    url (r'^clientdelete/(?P<pk>\d+)$', view=ClientDeleteView.as_view(), name='client_delete'),
    url (r'^clientdetail/(?P<pk>\d+)$', view=ClientDetailView.as_view(), name='client_detail'),    
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
    url (r'^estatecreateclient/(?P<client>\d+)$', view=EstateCreateClientView.as_view(), name='estate_create_client'),
    url (r'^estateupdate/(?P<pk>\d+)$', view=EstateUpdateView.as_view(), name='estate_update'),        
    url (r'^estatedelete/(?P<pk>\d+)$', view=EstateDeleteView.as_view(), name='estate_delete'),
    url (r'^estatecommupdate/(?P<pk>\d+)$', view=EstateCommunicationUpdateView.as_view(), name='estate_comm_update'),    
    url (r'^estateparamsupdate/(?P<pk>\d+)$', view=EstateParamUpdateView.as_view(), name='estate_params_update'),
    url (r'^estateimages/(?P<estate>\d+)$', view=EstateImagesView.as_view(), name='estate_images'),
)

urlpatterns += patterns('',
    url (r'^estatedetail/(?P<pk>\d+)$', view=EstateDetailView.as_view(), name='estate_detail'),
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
    url (r'^imageswap/(?P<estate>\d+)/(?P<pk>\d+)/(?P<direction>\w+)$', view=SwapEstatePhotoView.as_view(), name='image_swap'),
    url (r'^imageupdate/(?P<pk>\d+)$', view=ImageUpdateView.as_view(), name='image_update'),
    url (r'^imagedelete/(?P<pk>\d+)$', view=ImageDeleteView.as_view(), name='image_delete'),    
)

urlpatterns += patterns('',
    url (r'^steadupdate/(?P<pk>\d+)/(?P<estate>\d+)$', SteadUpdateView.as_view(), name='stead_update'),     
) 

urlpatterns += patterns('',
    url (r'^selectestatetype/$', EstateTypeViewAjax.as_view(), name='select_estate_type'),
    url (r'^selectplaceabletype/(?P<estate>\d+)$', PlaceableTypeViewAjax.as_view(), name='select_placeable_type'),    
    url (r'^bidgappend/(?P<estate>\d+)/(?P<estate_type>\d+)$', BidgAppendView.as_view(), name='bidg_append'),    
    url (r'^bidgremove/(?P<pk>\d+)$', BidgRemoveView.as_view(), name='bidg_remove'),     
)

urlpatterns += patterns('',
    url (r'^registercreate/(?P<bid>\d+)$', EstateRegisterCreateView.as_view(), name='register_create'),      
    url (r'^registerupdate/(?P<pk>\d+)$', EstateRegisterUpdateView.as_view(), name='register_update'),
    url (r'^registerdelete/(?P<pk>\d+)$', EstateRegisterDeleteView.as_view(), name='register_delete'),
    url (r'^registerdetail/(?P<pk>\d+)$', EstateRegisterDetailView.as_view(), name='register_detail'),
    url (r'^registerlist/$', EstateRegisterListView.as_view(), name='register_list'),
    url (r'^registeraddestate/(?P<pk>\d+)/(?P<estate_pk>\d+)$', AddEstateToRegisterView.as_view(), name='register_add_estate'),
    url (r'^registerremoveestate/(?P<pk>\d+)/(?P<estate_pk>\d+)$', RemoveEstateFromRegisterView.as_view(), name='register_remove_estate'),
    url (r'^registerselect/(?P<bid_pk>\d+)$', EstateRegisterSelectView.as_view(), name='register_select'),
    url (r'^registeraddbid/(?P<pk>\d+)/(?P<bid_pk>\d+)$', AddRegisterToBid.as_view(), name='register_add_bid'),
    url (r'^registerremovebid/(?P<pk>\d+)/(?P<bid_pk>\d+)$', RemoveRegisterFromBid.as_view(), name='register_remove_bid'),
        
)

urlpatterns += patterns('',    
    url (r'^bidcreate/(?P<client>\d+)$', BidCreateView.as_view(), name='bid_create'),    
    url (r'^bidcreate/$', BidCreateView.as_view(), name='bid_create'),
    url (r'^bidupdate/(?P<pk>\d+)$', BidUpdateView.as_view(), name='bid_update'),
    url (r'^bidremove/(?P<pk>\d+)$', BidDeleteView.as_view(), name='bid_remove'),
    url (r'^bidlist/$', BidListView.as_view(), name='bid_list'),       
    url (r'^biddetail/(?P<pk>\d+)$', BidDetailView.as_view(), name='bid_detail'),             
)
