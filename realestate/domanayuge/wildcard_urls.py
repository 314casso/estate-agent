# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, url, include
from domanayuge.views import DevPage, Project, Blog, Article, MapPage, Case, CaseList,\
    send_email, robots, DevList, DevPriceList, DevPrice, stroyka_sitemap,\
    DevelopServices, PrivacyPolicyPage
import settings

handler404 = 'domanayuge.views.custom_page_not_found_view'

admin.autodiscover()

urlpatterns = patterns('',   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^content_edit/', include('content_edit.urls')),
    url(r'^$', DevPage.as_view() ,name='devpage'),
    url(r'^projects/(?P<key>[-\w]+)/$', DevList.as_view(), name='projects'),
    url(r'^projects/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', Project.as_view(), name='project'),
    url(r'^blog/$', Blog.as_view(), name='blog'),
    url(r'^karta-doma-na-yuge/$', MapPage.as_view(), {"sitemap_source": stroyka_sitemap}, name='karta-doma-na-yuge'),
    url(r'^blog/(?P<slug>[-\w]+)/$', Article.as_view(), name='page'),
    url(r'^cases/(?P<key>[-\w]+)/$', CaseList.as_view(), name='cases'),
    url(r'^cases/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', Case.as_view(), name='case'),
    url(r'^sendemail/$', send_email, name='send_email'),
    url(r'^prices/(?P<key>[-\w]+)/$', DevPriceList.as_view(), name='prices'),
    url(r'^prices/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', DevPrice.as_view(), name='price'),
    url(r'^developservices/(?P<key>[-\w]+)/$', DevelopServices.as_view(), name='developservices'),
    url(r'^developservice/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', DevPrice.as_view(), name='developservice'),
    url(r'^privacy-policy/', PrivacyPolicyPage.as_view(), name='privacy-policy')
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