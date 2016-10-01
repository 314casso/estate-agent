from django.conf.urls import patterns, url, include
from django.contrib import admin
import settings
from domanayuge.views import HomePage, send_email

admin.autodiscover()

urlpatterns = patterns('',    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePage.as_view() ,name='home'),
    url(r'^content_edit/', include('content_edit.urls')),
    url(r'^sendemail/$', send_email, name='send_email'),
    
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))