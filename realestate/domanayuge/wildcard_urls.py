# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, url, include
from domanayuge.views import DevPage, Project, Blog, Article, Case, CaseList,\
    send_email, robots, DevList, DevPriceList, DevPrice, stroyka_sitemap
import settings


admin.autodiscover()

urlpatterns = patterns('',   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^content_edit/', include('content_edit.urls')),
    url(r'^$', DevPage.as_view() ,name='devpage'),
    url(r'^projects/(?P<key>[-\w]+)/$', DevList.as_view(), name='projects'),
    url(r'^projects/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', Project.as_view(), name='project'),
    url(r'^blog/$', Blog.as_view(), name='blog'),
    url(r'^blog/(?P<slug>[-\w]+)/$', Article.as_view(), name='page'),
    url(r'^cases/(?P<key>[-\w]+)/$', CaseList.as_view(), name='cases'),
    url(r'^cases/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', Case.as_view(), name='case'),
    url(r'^sendemail/$', send_email, name='send_email'),
    url(r'^prices/(?P<key>[-\w]+)/$', DevPriceList.as_view(), name='prices'),
    url(r'^prices/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', DevPrice.as_view(), name='price'),
)
  

urlpatterns += patterns('',
        url(r'^sitemap\.xml$', stroyka_sitemap, name='domanayuge.views.stroyka_sitemap'),        
        url(r'^robots\.txt$', robots),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))