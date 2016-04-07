from django.conf.urls.defaults import patterns, include, url
from estatebase.views import ClientListView, \
    ClientCreateView, ClientUpdateView, ClientDeleteView, ContactHistoryListView, \
    ContactUpdateView, ClientSelectView, ClientUpdateEstateView, \
    ClientRemoveEstateView, EstateCommunicationUpdateView, \
    EstateParamUpdateView, EstateUpdateView, ApartmentCreateView, \
    ApartmentUpdateView, LevelCreateView, LevelUpdateView, LevelDeleteView, \
    upload_images, EstateImagesView, SwapEstatePhotoView, ImageUpdateView, \
    ImageDeleteView, EstateDetailView, SteadUpdateView, EstateTypeViewAjax, \
    BidgAppendView, BidgRemoveView, EstateListDetailsView, PlaceableTypeViewAjax,\
    BidCreateView, BidUpdateView, BidListView, BidDeleteView,\
    ClientDetailView, EstateDeleteView, BidDetailView, EstateRegisterCreateView,\
    EstateRegisterUpdateView, EstateRegisterDeleteView, EstateSelectRegisterView,\
    EstateRegisterDetailView, AddEstateToRegisterView,\
    RemoveEstateFromRegisterView, EstateRegisterListView,\
    EstateRegisterSelectView, AddRegisterToBid, RemoveRegisterFromBid,\
    EstateCreateClientView, RegisterReportView, SteadAppendView, SteadRemoveView,\
    ClientStatusUpdateView, EstateCreateWizardView, RestoreClientView,\
    BidEventCreateView, BidEventUpdateView, BidEventDeleteView,\
    EstateRegisterBindView, MultiBindEstateToRegister, WordpressQueue,\
    estate_list_contacts, bid_list_contacts, client_list_contacts, incorrect_contacts,\
    ClientPartnerRemoveView, ClientUpdateBidView, ClientBidSelectView,\
    set_bid_basic_client, ManageEstateM2MEntrance, upload_files,\
    FileDeleteView, FileUpdateView, GenericFilesView

urlpatterns = patterns('',   
    url(r'^estatelist/$',EstateListDetailsView.as_view(), name='estate-list'),
    url(r'^estateselectlist/(?P<selected>\d+)$',EstateSelectRegisterView.as_view(template_name='estate_to_register.html'), name='estate_select_list'),
    url(r'^estateselectlist/(?P<pk>\d+)/(?P<selected>\d+)$',EstateSelectRegisterView.as_view(template_name='estate_to_register.html'), name='estate_select_list'),
    url(r'^estatelistdetails/(?P<pk>\d+)$',EstateListDetailsView.as_view(), name='estate_list_details'),
    url(r'^selectable/', include('selectable.urls')),    
    url(r'^clients/$',ClientListView.as_view(), name='client-list'),
    url(r'^clients/(?P<estate_pk>\d+)$',ClientSelectView.as_view(), name='client_select'),
    url(r'^clientsbid/(?P<bid_pk>\d+)$',ClientBidSelectView.as_view(), name='client_bid_select'),
    url (r'^clientcreate/$', view=ClientCreateView.as_view(), name='client_create'),
    url (r'^clientcreatepopup/$', view=ClientCreateView.as_view(template_name='clients/client_popup_form.html'), name='client_create_popup'),
    url (r'^clientupdate/(?P<pk>\d+)$', view=ClientUpdateView.as_view(), name='client_update'),
    url (r'^clientdelete/(?P<pk>\d+)$', view=ClientDeleteView.as_view(), name='client_delete'),
    url (r'^clientdetail/(?P<pk>\d+)$', view=ClientDetailView.as_view(), name='client_detail'),
    url (r'^clientstatus/(?P<estate>\d+)/(?P<client>\d+)$', view=ClientStatusUpdateView.as_view(), name='client_status'),
)

urlpatterns += patterns('',
    url (r'^contacthistory/(?P<pk>\d+)/$', ContactHistoryListView.as_view(), name='contact_history' ),        
    url (r'^contactupdate/(?P<pk>\d+)/$', ContactUpdateView.as_view(), name='contact_update' ),
)
 
urlpatterns += patterns('',
    url (r'^clientestate/(?P<pk>\d+)/(?P<estate_pk>\d+)$', ClientUpdateEstateView.as_view(), name='client_estate'),   
    url (r'^clientestateunbind/(?P<pk>\d+)/(?P<estate_pk>\d+)$', ClientRemoveEstateView.as_view(), name='client_estate_unbind'),
    url (r'^clientrestore/(?P<pk>\d+)$', RestoreClientView.as_view(), name='client_restore'),
) 

urlpatterns += patterns('',
    url (r'^estatecreate/(?P<estate_type>\d+)$', view=EstateCreateWizardView.as_view(), name='estate_create'),
    url (r'^estatecreateclient/(?P<client>\d+)$', view=EstateCreateClientView.as_view(), name='estate_create_client'),
    url (r'^estateupdate/(?P<pk>\d+)$', view=EstateUpdateView.as_view(), name='estate_update'),        
    url (r'^estatedelete/(?P<pk>\d+)$', view=EstateDeleteView.as_view(), name='estate_delete'),
    url (r'^estatecommupdate/(?P<pk>\d+)$', view=EstateCommunicationUpdateView.as_view(), name='estate_comm_update'),    
    url (r'^estateparamsupdate/(?P<pk>\d+)$', view=EstateParamUpdateView.as_view(), name='estate_params_update'),
    url (r'^estateimages/(?P<estate>\d+)$', view=EstateImagesView.as_view(), name='estate_images'),
    url (r'^genericfiles/(?P<model_key>\w+)/(?P<object_pk>\d+)$', view=GenericFilesView.as_view(), name='generic_files'),
    url (r'^estateentrances/(?P<pk>\d+)$', view=ManageEstateM2MEntrance.as_view(), name='manage_entrances'),
    
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
    url (r'^uploadfiles/$', view=upload_files, name='upload_files'),
    url (r'^imageswap/(?P<estate>\d+)/(?P<pk>\d+)/(?P<direction>\w+)$', view=SwapEstatePhotoView.as_view(), name='image_swap'),
    url (r'^imageupdate/(?P<pk>\d+)$', view=ImageUpdateView.as_view(), name='image_update'),
    url (r'^imagedelete/(?P<pk>\d+)$', view=ImageDeleteView.as_view(), name='image_delete'),
    url (r'^filedelete/(?P<pk>\d+)$', view=FileDeleteView.as_view(), name='file_delete'),
    url (r'^fileupdate/(?P<pk>\d+)$', view=FileUpdateView.as_view(), name='file_update'),        
)

urlpatterns += patterns('',
    url (r'^steadupdate/(?P<pk>\d+)/(?P<estate>\d+)$', SteadUpdateView.as_view(), name='stead_update'),
    url (r'^steadappend/(?P<estate>\d+)$', SteadAppendView.as_view(), name='stead_append'),    
    url (r'^steadremove/(?P<pk>\d+)$', SteadRemoveView.as_view(), name='stead_remove'),     
) 

urlpatterns += patterns('',
    url (r'^selectestatetype/$', EstateTypeViewAjax.as_view(), name='select_estate_type'),
    url (r'^selectplaceabletype/(?P<estate>\d+)$', PlaceableTypeViewAjax.as_view(), name='select_placeable_type'),    
    url (r'^bidgappend/(?P<estate>\d+)/(?P<estate_type>\d+)$', BidgAppendView.as_view(), name='bidg_append'),    
    url (r'^bidgremove/(?P<pk>\d+)$', BidgRemoveView.as_view(), name='bidg_remove'),     
)

urlpatterns += patterns('',
    url (r'^registercreatefree/$', EstateRegisterCreateView.as_view(), name='register_create_free'),
    url (r'^registercreate/(?P<bid>\d+)$', EstateRegisterCreateView.as_view(), name='register_create'),      
    url (r'^registerupdate/(?P<pk>\d+)$', EstateRegisterUpdateView.as_view(), name='register_update'),
    url (r'^registerdelete/(?P<pk>\d+)$', EstateRegisterDeleteView.as_view(), name='register_delete'),
    url (r'^registerdetail/(?P<pk>\d+)$', EstateRegisterDetailView.as_view(), name='register_detail'),
    url (r'^registerlist/$', EstateRegisterListView.as_view(), name='register-list'),
    url (r'^registeraddestate/(?P<pk>\d+)/(?P<estate_pk>\d+)$', AddEstateToRegisterView.as_view(), name='register_add_estate'),
    url (r'^registerremoveestate/(?P<pk>\d+)/(?P<estate_pk>\d+)$', RemoveEstateFromRegisterView.as_view(), name='register_remove_estate'),
    url (r'^registerselect/(?P<bid_pk>\d+)$', EstateRegisterSelectView.as_view(), name='register_select'),
    url (r'^registeraddbid/(?P<pk>\d+)/(?P<bid_pk>\d+)$', AddRegisterToBid.as_view(), name='register_add_bid'),
    url (r'^registerremovebid/(?P<pk>\d+)/(?P<bid_pk>\d+)$', RemoveRegisterFromBid.as_view(), name='register_remove_bid'),
    url (r'^registerbind/(?P<estate>\d+)$', EstateRegisterBindView.as_view(), name='register_bind'),
    url (r'^registermultibind/(?P<estate>\d+)/(?P<action>\d+)$', MultiBindEstateToRegister.as_view(), name='register_multi_bind'),
    
)

urlpatterns += patterns('',    
    url (r'^bidcreate/(?P<client>\d+)$', BidCreateView.as_view(), name='bid_create'),    
    url (r'^bidcreate/$', BidCreateView.as_view(), name='bid_create'),
    url (r'^bidupdate/(?P<pk>\d+)$', BidUpdateView.as_view(), name='bid_update'),
    url (r'^bidremove/(?P<pk>\d+)$', BidDeleteView.as_view(), name='bid_remove'),
    url (r'^bidlist/$', BidListView.as_view(), name='bid-list'),       
    url (r'^biddetail/(?P<pk>\d+)$', BidDetailView.as_view(), name='bid_detail'),
    url (r'^bideventupdate/(?P<pk>\d+)$', BidEventUpdateView.as_view(), name='bid_event_update'),
    url (r'^bideventcreate/(?P<bid>\d+)$', BidEventCreateView.as_view(), name='bid_event_create'),
    url (r'^bideventdelete/(?P<pk>\d+)$', BidEventDeleteView.as_view(), name='bid_event_delete'),
    url (r'^clientbid/(?P<pk>\d+)/(?P<bid_pk>\d+)$', ClientUpdateBidView.as_view(), name='client_bid_bind'),
    url (r'^clientbidunbind/(?P<pk>\d+)/(?P<bid_pk>\d+)$', ClientPartnerRemoveView.as_view(), name='client_bid_unbind'),
    url (r'^setbidbasicclient/(?P<client_pk>\d+)/(?P<bid_pk>\d+)$', view=set_bid_basic_client, name='set_bid_basic_client'),
    
)

urlpatterns += patterns('',    
    url (r'^privateshortreport/(?P<pk>\d+)$', RegisterReportView.as_view(template_name='reports/private_short.html'), name='private_short_report'),
    url (r'^privatedetailreport/(?P<pk>\d+)$', RegisterReportView.as_view(template_name='reports/private_detail.html'), name='private_detail_report'),
    url (r'^publicreport/(?P<pk>\d+)$', RegisterReportView.as_view(template_name='reports/public.html'), name='public_report'),
    url (r'^orbitareport/(?P<pk>\d+)$', RegisterReportView.as_view(template_name='reports/newspapers/orbita.html'), name='orbita_report'),
)

urlpatterns += patterns('',    
    url (r'^wordpressqueue/$', WordpressQueue.as_view(), name='wordpress_queue'),
)

urlpatterns += patterns('',    
    url (r'^estatelistcontacts/(?P<contact_type_pk>\d+)$', view=estate_list_contacts, name='estate_list_contacts'),
    url (r'^bidlistcontacts/(?P<contact_type_pk>\d+)$', view=bid_list_contacts, name='bid_list_contacts'),
    url (r'^clientlistcontacts/(?P<contact_type_pk>\d+)$', view=client_list_contacts, name='client_list_contacts'),
    url (r'^incorrectcontacts/$', view=incorrect_contacts, name='incorrect_contacts'),
)