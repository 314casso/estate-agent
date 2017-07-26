from django.conf import settings
from django_hosts import patterns, host
from domanayuge.models import LocalityDomain


def locality_callback(request, domain):
    request.domain_pattern = domain
    try:
        domain_obj = LocalityDomain.objects.get(domain=domain)
    except LocalityDomain.DoesNotExist:
        domain_obj = None
    request.domain = domain_obj


host_patterns = patterns('',
                         host(r'^$', settings.ROOT_URLCONF, name='home'),
                         host(r'(domanayuge|www)',
                              settings.ROOT_URLCONF, name='www'),
                         host(r'(?P<domain>remont|anaparemont|temrukremont|nvrskremont|gzhkremont)', 'domanayuge.remont_urls', 
                              name='remont', callback='domanayuge.hosts.locality_callback'),                    
                         host(r'(?P<domain>\w+)', 'domanayuge.wildcard_urls',
                              name='wildcard', callback='domanayuge.hosts.locality_callback'),
                        )