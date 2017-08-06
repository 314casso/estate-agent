from django.conf import settings
from django_hosts import patterns, host
from domanayuge.models import LocalityDomain
from django.contrib.sites.models import Site


def locality_callback(request, domain):
    request.domain_pattern = domain
    try:
        domain_obj = LocalityDomain.objects.get(domain=domain)
    except LocalityDomain.DoesNotExist:
        domain_obj = None
    request.domain = domain_obj
    try:
        site = Site.objects.get(name=domain)
        settings.SITE_ID = site.id
    except Site.DoesNotExist:
        pass
            
host_patterns = patterns('',
                         host(r'^$', settings.ROOT_URLCONF, name='home'),
                         host(r'(domanayuge|www)',
                              settings.ROOT_URLCONF, name='www'),
                         host(r'(?P<domain>remont|anaparemont|temrukremont|nvrskremont|gzhkremont)', 'domanayuge.remont_urls', 
                              name='remont', callback='domanayuge.hosts.locality_callback'),                    
                         host(r'(?P<domain>\w+)', 'domanayuge.wildcard_urls',
                              name='wildcard', callback='domanayuge.hosts.locality_callback'),
                        )