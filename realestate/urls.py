from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings
from django.conf.urls.static import static


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
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)