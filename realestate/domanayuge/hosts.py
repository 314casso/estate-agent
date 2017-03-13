from django.conf import settings
from django_hosts import patterns, host
from domanayuge.models import LocalityDomain


def locality_callback(request, domain):
    try:
        domain = LocalityDomain.objects.get(domain=domain)
    except LocalityDomain.DoesNotExist:
        domain = None
    request.domain = domain
    

host_patterns = patterns('',
    host(r'^$', settings.ROOT_URLCONF, name='home'),
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'(?P<domain>\w+)', 'domanayuge.wildcard_urls', name='wildcard', callback='domanayuge.hosts.locality_callback'),
)