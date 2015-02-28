from django.conf.urls.defaults import patterns, url
from devrep.views import PartnerListView, PartnerCreateView

urlpatterns = patterns('',    
    url (r'^partners/$', PartnerListView.as_view(), name='partner_list'),
    url (r'^partnercreate/$', view=PartnerCreateView.as_view(), name='partner_create'),
)