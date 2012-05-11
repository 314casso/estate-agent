from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from estatebase.views import EstateTypeView, EstateCreateView, EstateListView, EstateUpdateView,\
    ClientListView


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
    url(r'^clients/$',ClientListView.as_view(), name='client_table'),
)


       
