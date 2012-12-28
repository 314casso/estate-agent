from django.http import QueryDict
import re
from decimal import Decimal
from urlparse import urlparse

def safe_next_link(full_path):
    q = QueryDict('', mutable=True)        
    #q['next'] = full_path
    next_query = QueryDict(urlparse(full_path).query).get('next', None)
    if next_query:        
        next_url = urlparse(next_query).path
        next_query_dict = QueryDict(urlparse(next_query).query).copy()
        print next_query_dict
        for k,v in next_query_dict.iteritems():          
            if not v:
                next_query_dict.pop(k)                          
        q['next'] = u'%s?%s' % (next_url, next_query_dict.urlencode())             
    return q.urlencode(safe='/')

def parse_decimal(value, splitter=None, index=1):
    pattern = u"[^\d,.-/'%s]" % (splitter or '')    
    r = re.compile(pattern)    
    value = r.sub('', value)
    value = value.replace(',','.').replace("'",'.')    
    if not value:
        return None
    if splitter:    
        parts = value.split(splitter);    
        result = parts[0] if len(parts) == 1 else parts[index]
        if result:
            result = Decimal(result)                       
            if 0 < result < 999:
                return result
    else:
        return Decimal(value)

def split_digit(values):
    result = []
    parts = re.split('\D', values)
    for part in parts:
        if part.isdigit(): 
            result.append(part)
    return result
    
                          
#print parse_decimal("2, 5")        