from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from realestate.estatebase.views import EstateTypeView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'realestate.views.home', name='home'),
    # url(r'^realestate/', include('realestate.foo.urls')),    
    
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('',
    (r'^cat/$', EstateTypeView.as_view()),
)