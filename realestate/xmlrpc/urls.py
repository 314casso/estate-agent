from django.conf.urls.defaults import patterns
from xmlrpc.views import rpc_handler

urlpatterns = patterns('',
    (r'^lot$', rpc_handler),
)