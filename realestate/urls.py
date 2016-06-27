from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('',    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^estatebase/', include('estatebase.urls')),  
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',name='login'),     
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'session_security/', include('session_security.urls')),
    url(r'^devrep/', include('devrep.urls')),
    url(r'^xmlrpc/', include('xmlrpc.urls')),
    url(r'^export/', include('exportdata.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
