# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, url, include
from domanayuge.views import Blog, Article, MapPage, PrivacyPolicyPage, \
    send_email, robots,\
    PogrebPage, PogrebCase, PogrebList, PogrebCaseList,\
    pogreb_sitemap, PogrebPriceList, PogrebPrice, TermsOfUse
import settings
from domanayuge.models import ContentEntry


admin.autodiscover()

handler404 = 'domanayuge.views.custom_page_not_found_view'

urlpatterns = patterns('',   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^content_edit/', include('content_edit.urls')),
    url(r'^$', PogrebPage.as_view() ,name='septikpage'),
    url(r'^projects/(?P<key>[-\w]+)/$', PogrebList.as_view(), name='projects'),
    url(r'^prices/(?P<key>[-\w]+)/$', PogrebPriceList.as_view(), name='prices'),
    url(r'^price/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', PogrebPrice.as_view(), name='price'),        
    url(r'^blog/$', Blog.as_view(), name='blog'),
    url(r'^blog/(?P<slug>[-\w]+)/$', Article.as_view(), name='page'),
    url(r'^cases/(?P<key>[-\w]+)/$', PogrebCaseList.as_view(), name='cases'),
    url(r'^pictures/(?P<key>[-\w]+)/$', PogrebCaseList.as_view(), name='pictures'),
    url(r'^cases/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', PogrebCase.as_view(), name='case'),
    url(r'^sendemail/$', send_email, name='send_email'),
    url(r'^karta-doma-na-yuge/$', MapPage.as_view(), {"sitemap_source": pogreb_sitemap}, name='karta-doma-na-yuge'),
    url(r'^terms-of-use/', TermsOfUse.as_view(), name='terms_use_page'),
    url(r'^privacy-policy/', PrivacyPolicyPage.as_view(), name='privacy-policy')
)


blog_dict = {
    'queryset': ContentEntry.objects.filter(categories__slug="blog", tags__contained_by=[u'погреб']),
    'date_field': 'publication_date',
}


urlpatterns += patterns('',
        url(r'^sitemap\.xml$', pogreb_sitemap, name='domanayuge.views.pogreb_sitemap'),        
        url(r'^robots\.txt$', robots),
)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))