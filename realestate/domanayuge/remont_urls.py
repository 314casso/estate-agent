# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns, url, include
from domanayuge.views import ProjectList, Project, Blog, Article, Case, CaseList,\
    send_email, robots_stroyka, RemontPage
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from domanayuge.sitemaps import StaticViewSitemap
import settings
from domanayuge.models import ContentEntry

admin.autodiscover()

urlpatterns = patterns('',   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^content_edit/', include('content_edit.urls')),
    url(r'^$', RemontPage.as_view() ,name='remontpage'),
    url(r'^projects/(?P<key>[-\w]+)/$', ProjectList.as_view(), name='projects'),
    url(r'^projects/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', Project.as_view(), name='project'),
    url(r'^blog/$', Blog.as_view(), name='blog'),
    url(r'^blog/(?P<slug>[-\w]+)/$', Article.as_view(), name='page'),
    url(r'^cases/(?P<key>[-\w]+)/$', CaseList.as_view(), name='cases'),
    url(r'^cases/(?P<key>[-\w]+)/(?P<slug>[-\w]+)/$', Case.as_view(), name='case'),
    url(r'^sendemail/$', send_email, name='send_email'),
)

blog_dict = {
    'queryset': ContentEntry.objects.filter(categories__slug="blog", tags__contained_by=[u'строительство', u'ремонт']),
    'date_field': 'publication_date',
}

urlpatterns += patterns('',
        url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {
                        'blog': GenericSitemap(blog_dict, priority=0.6),                        
                        'static': StaticViewSitemap 
                      }
        },
        name='django.contrib.sitemaps.views.sitemap'),        
        url(r'^robots\.txt$', robots_stroyka),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))