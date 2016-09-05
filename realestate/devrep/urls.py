from django.conf.urls import patterns, url, include
from devrep.views import PartnerListView, PartnerCreateView, PartnerDetailView,\
    PartnerDeleteView, PartnerUpdateView, ClientPartnerUpdateView,\
    ClientPartnerRemoveView, ClientPartnerSelectView,\
    ClientPartnerThroughUpdateView, GearCreateView, DevProfileCreateView,\
    DevProfileUpdateView, ExtraProfileCreateView, ExtraProfileUpdateView,\
    DevProfileDeleteView, DevProfileDetailView, PartnerSelectView,\
    ManageDevProfileM2MWorktype, ManageDevProfileM2MGoods


urlpatterns = patterns('',    
    url (r'^partners/$', PartnerListView.as_view(), name='partner_list'),
    url (r'^partnercreate/$', view=PartnerCreateView.as_view(), name='partner_create'),
    url (r'^partnerupdate/(?P<pk>\d+)$', view=PartnerUpdateView.as_view(), name='partner_update'),
    url (r'^partnerdetail/(?P<pk>\d+)$', view=PartnerDetailView.as_view(), name='partner_detail'),
    url (r'^partnerdelete/(?P<pk>\d+)$', view=PartnerDeleteView.as_view(), name='partner_delete'),
    url (r'^partnerselect/(?P<client_pk>\d+)$', view=PartnerSelectView.as_view(), name='partner_select'),
        
)

urlpatterns += patterns('',
    url(r'^clientsbid/(?P<partner_pk>\d+)$',ClientPartnerSelectView.as_view(), name='client_partner_select'),
    url (r'^clientpartnerbind/(?P<pk>\d+)/(?P<partner_pk>\d+)$', ClientPartnerUpdateView.as_view(), name='client_partner_bind'),
    url (r'^clientpartnerunbind/(?P<pk>\d+)/(?P<partner_pk>\d+)$', ClientPartnerRemoveView.as_view(), name='client_partner_unbind'),
    url (r'^clientpartnerthroughupdate/(?P<client>\d+)/(?P<partner>\d+)$', ClientPartnerThroughUpdateView.as_view(), name='client_partner_through_update'),
    url (r'^gearcreatepopup/$', view=GearCreateView.as_view(template_name='simple_popup_form.html'), name='gear_create_popup'),
)

urlpatterns += patterns('',
    url(r'^devprofilecreate/(?P<client_pk>\d+)$',DevProfileCreateView.as_view(), name='dev_profile_create'),    
    url(r'^devprofileupdate/(?P<pk>\d+)$',DevProfileUpdateView.as_view(), name='dev_profile_update'),
    url(r'^devprofiledelete/(?P<pk>\d+)$',DevProfileDeleteView.as_view(), name='dev_profile_delete'),
    url(r'^devprofiledetail/(?P<pk>\d+)$',DevProfileDetailView.as_view(), name='dev_profile_detail'),    
    url(r'^managegoodsprofile/(?P<pk>\d+)$',ManageDevProfileM2MGoods.as_view(), name='manage_goods_profile'),   
    url(r'^manageworktypeprofile/(?P<pk>\d+)$',ManageDevProfileM2MWorktype.as_view(), name='manage_worktype_profile'),
    
)

urlpatterns += patterns('',
    url(r'^extraprofilecreate/(?P<client_pk>\d+)$',ExtraProfileCreateView.as_view(), name='extra_profile_create'),    
    url(r'^extraprofileupdate/(?P<pk>\d+)$',ExtraProfileUpdateView.as_view(), name='extra_profile_update'),
)