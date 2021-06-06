# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, url, include
from domanayuge.views import Blog, Article, MapPage, \
    send_email, robots, rodlex_sitemap, \
    RodlexPage,\
    RodlexList, RodlexPriceList, RodlexPrice, RodlexCaseList, RodlexCase    
import settings
from domanayuge.models import ContentEntry


admin.autodiscover()


urlpatterns = patterns('',   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^content_edit/', include('content_edit.urls')),
    url(r'^$', RodlexPage.as_view() ,name='rodlexpage'),
    url(r'^projects/(?P<key>[-\w]+)/$', RodlexList.as_view(), name='projects'),
    url(r'^prices/(?P<key>[-\w]+)/$', RodlexPriceList.as_view(), name='prices'),
    url(r'^price/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', RodlexPrice.as_view(), name='price'),        
    url(r'^blog/$', Blog.as_view(), name='blog'),
    url(r'^blog/karta-doma-na-yuge/$', MapPage.as_view(), {"sitemap_source": rodlex_sitemap}, name='karta-doma-na-yuge'),
    url(r'^videoblog/$', VideoBlog.as_view(), name='videoblog'),
    url(r'^blog/(?P<slug>[-\w]+)/$', Article.as_view(), name='page'),
    url(r'^cases/(?P<key>[-\w]+)/$', RodlexCaseList.as_view(), name='cases'),
    url(r'^pictures/(?P<key>[-\w]+)/$', RodlexCaseList.as_view(), name='pictures'),
    url(r'^cases/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', RodlexCase.as_view(), name='case'),
    url(r'^sendemail/$', send_email, name='send_email'),
    url(r'^term-of-use/', views.get_terms_use),
    url(r'^privacy-policy/', views.get_privacy_policy),
)


blog_dict = {
    'queryset': ContentEntry.objects.filter(categories__slug="blog", tags__contained_by=[u'родлекс']),
    'date_field': 'publication_date',
}


urlpatterns += patterns('',
        url(r'^sitemap\.xml$', rodlex_sitemap, name='domanayuge.views.septik_sitemap'),        
        url(r'^robots\.txt$', robots),
)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
