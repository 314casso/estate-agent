from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from realestate.estatebase.views import EstateTypeView, EstateCreateView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'realestate.views.home', name='home'),
    # url(r'^realestate/', include('realestate.foo.urls')),    
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cat/$', EstateTypeView.as_view(), name='estate_list'),
    url (r'^create/(?P<estate_type>\d+)$', view=EstateCreateView.as_view(), name='estate_create'),
    (r'^selectable/', include('selectable.urls')),
)


       
