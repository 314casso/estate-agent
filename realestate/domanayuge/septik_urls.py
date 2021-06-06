# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, url, include
from domanayuge.views import Blog, Article, MapPage, \
    send_email, robots,\
    SeptikPage, SeptikCase, SeptikList, SeptikCaseList,\
    septik_sitemap, SeptikPriceList, SeptikPrice, SeptikBaseCaseList
import settings
from domanayuge.models import ContentEntry


admin.autodiscover()


urlpatterns = patterns('',   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^content_edit/', include('content_edit.urls')),
    url(r'^$', SeptikPage.as_view() ,name='septikpage'),
    url(r'^projects/(?P<key>[-\w]+)/$', SeptikList.as_view(), name='projects'),
    url(r'^prices/(?P<key>[-\w]+)/$', SeptikPriceList.as_view(), name='prices'),
    url(r'^price/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', SeptikPrice.as_view(), name='price'),        
    url(r'^blog/$', Blog.as_view(), name='blog'),
    url(r'^blog/karta-doma-na-yuge/$', MapPage.as_view(), {"sitemap_source": septik_sitemap}, name='karta-doma-na-yuge'),
    url(r'^videoblog/$', VideoBlog.as_view(), name='videoblog'),
    url(r'^blog/(?P<slug>[-\w]+)/$', Article.as_view(), name='page'),
    url(r'^cases/(?P<key>[-\w]+)/$', SeptikCaseList.as_view(), name='cases'),
    url(r'^pictures/(?P<key>[-\w]+)/$', SeptikBaseCaseList.as_view(), name='pictures'),
    url(r'^cases/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', SeptikCase.as_view(), name='case'),
    url(r'^sendemail/$', send_email, name='send_email'),
    url(r'^term-of-use/', views.get_terms_use),
    url(r'^privacy-policy/', views.get_privacy_policy),
#     url(r'^renovationservices/(?P<key>[-\w]+)/$', RemontRenovationServices.as_view(), name='renovationservices'),
#     url(r'^renovationservice/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', RemontPrice.as_view(), name='renovationservice'),
)


blog_dict = {
    'queryset': ContentEntry.objects.filter(categories__slug="blog", tags__contained_by=[u'септик']),
    'date_field': 'publication_date',
}


urlpatterns += patterns('',
        url(r'^sitemap\.xml$', septik_sitemap, name='domanayuge.views.septik_sitemap'),        
        url(r'^robots\.txt$', robots),
)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
