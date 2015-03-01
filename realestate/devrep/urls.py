from django.conf.urls.defaults import patterns, url
from devrep.views import PartnerListView, PartnerCreateView, PartnerDetailView,\
    PartnerDeleteView, PartnerUpdateView

urlpatterns = patterns('',    
    url (r'^partners/$', PartnerListView.as_view(), name='partner_list'),
    url (r'^partnercreate/$', view=PartnerCreateView.as_view(), name='partner_create'),
    url (r'^partnerupdate/(?P<pk>\d+)$', view=PartnerUpdateView.as_view(), name='partner_update'),
    url (r'^partnerdetail/(?P<pk>\d+)$', view=PartnerDetailView.as_view(), name='partner_detail'),
    url (r'^partnerdelete/(?P<pk>\d+)$', view=PartnerDeleteView.as_view(), name='partner_delete'),    
)