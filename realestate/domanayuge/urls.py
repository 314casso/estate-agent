from django.conf.urls import patterns, url, include
from django.contrib import admin
import settings
from domanayuge.views import HomePage, send_email, Blog, Article, MapPage, robots, TermsOfUse, PrivacyPolicyPage
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from domanayuge.models import ContentEntry
from domanayuge.sitemaps import StaticViewSitemap
from django.views.decorators.cache import never_cache


admin.autodiscover()

handler404 = 'domanayuge.views.custom_page_not_found_view'

urlpatterns = patterns('',    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePage.as_view(), name='home'),
    url(r'^content_edit/', include('content_edit.urls')),
    url(r'^sendemail/$', send_email, name='send_email'),
    url(r'^blog/$', Blog.as_view(), name='blog'),
    url(r'^blog/(?P<slug>[-\w]+)/$', Article.as_view(), name='page'),
    url(r'^karta-doma-na-yuge/$', MapPage.as_view(), name='karta-doma-na-yuge'),
    url(r'^terms-of-use/', TermsOfUse.as_view(), name='terms_use_page'),
    url(r'^privacy-policy/', PrivacyPolicyPage.as_view(), name='privacy-policy')
)

blog_dict = {
    'queryset': ContentEntry.objects.filter(categories__slug="blog"),
    'date_field': 'publication_date',
}

portfolio_dict = {
    'queryset': ContentEntry.objects.filter(categories__key="portfoliodev"),
    'date_field': 'publication_date',
}

urlpatterns += patterns('',
        url(r'^sitemap\.xml$', never_cache(sitemap),
        {'sitemaps': {
                        'blog': GenericSitemap(blog_dict, priority=0.6), 
                        #'portfolio': GenericSitemap(portfolio_dict, priority=0.6),
                        #'static': StaticViewSitemap 
                      }
        },
        name='django.contrib.sitemaps.views.sitemap'),        
        url(r'^robots\.txt$', robots),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))