# -*- coding: utf-8 -*-
from spyder_helper.models import SpiderMeta
from urlparse import urlparse

def join_strings(strings, delim=u''):
    if not strings:
        return None
    result = [x.strip() for x in strings if x.strip()]
    return delim.join(result)

def process_value_base(value, spider_name):
    print "processing... %s for spider %s" % (value, spider_name)              
    q = SpiderMeta.objects.filter(url=value,spider=spider_name).exclude(status=SpiderMeta.ERROR)
    if q:
        print '%s skiping...' % value
        return None    
    return value

def get_url_path(url):        
        if url:
            link = url if isinstance(url, basestring) else url[0]                 
            o = urlparse(link)
            return o.path