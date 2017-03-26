from django.conf.urls import patterns, url, include
from django.contrib import admin
import settings
from domanayuge.views import HomePage, send_email, Blog, Article

admin.autodiscover()

urlpatterns = patterns('',    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePage.as_view() ,name='home'),
    url(r'^content_edit/', include('content_edit.urls')),
    url(r'^sendemail/$', send_email, name='send_email'),
    url(r'^blog/$', Blog.as_view(), name='blog'),
    url(r'^blog/(?P<slug>[-\w]+)/$', Article.as_view(), name='page'),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))