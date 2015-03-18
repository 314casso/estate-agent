from django.conf.urls.defaults import patterns, url
from devrep.views import PartnerListView, PartnerCreateView, PartnerDetailView,\
    PartnerDeleteView, PartnerUpdateView, ClientPartnerUpdateView,\
    ClientPartnerRemoveView, ClientPartnerSelectView,\
    ClientPartnerThroughUpdateView, GearCreateView

urlpatterns = patterns('',    
    url (r'^partners/$', PartnerListView.as_view(), name='partner_list'),
    url (r'^partnercreate/$', view=PartnerCreateView.as_view(), name='partner_create'),
    url (r'^partnerupdate/(?P<pk>\d+)$', view=PartnerUpdateView.as_view(), name='partner_update'),
    url (r'^partnerdetail/(?P<pk>\d+)$', view=PartnerDetailView.as_view(), name='partner_detail'),
    url (r'^partnerdelete/(?P<pk>\d+)$', view=PartnerDeleteView.as_view(), name='partner_delete'),    
)

urlpatterns += patterns('',
    url(r'^clientsbid/(?P<partner_pk>\d+)$',ClientPartnerSelectView.as_view(), name='client_partner_select'),
    url (r'^clientpartnerbind/(?P<pk>\d+)/(?P<partner_pk>\d+)$', ClientPartnerUpdateView.as_view(), name='client_partner_bind'),
    url (r'^clientpartnerunbind/(?P<pk>\d+)/(?P<partner_pk>\d+)$', ClientPartnerRemoveView.as_view(), name='client_partner_unbind'),
    url (r'^clientpartnerthroughupdate/(?P<client>\d+)/(?P<partner>\d+)$', ClientPartnerThroughUpdateView.as_view(), name='client_partner_through_update'),
    url (r'^gearcreatepopup/$', view=GearCreateView.as_view(template_name='simple_popup_form.html'), name='gear_create_popup'),
)