from django.conf.urls import patterns, url
from domanayuge.views import DevPage

urlpatterns = patterns('',   
    url(r'^$', DevPage.as_view() ,name='devpage'),
)
