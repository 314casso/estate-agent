from django.http import QueryDict
import re
from decimal import Decimal
from urlparse import urlparse
from django.utils.encoding import iri_to_uri

def safe_next_link(full_path, keys_to_delete=[]):
    q = QueryDict('', mutable=True)      
    next_url = urlparse(full_path).path
    next_query = iri_to_uri(urlparse(full_path).query)
    next_query_dict = None   
    if next_query:      
        deleted_keys = []                    
        next_query_dict = QueryDict(next_query).copy()
        if keys_to_delete:
            deleted_keys.extend(keys_to_delete)
        for k,v in next_query_dict.iteritems():          
            if not v:
                deleted_keys.append(k)
        for key in deleted_keys:
            if key in next_query_dict:
                del[next_query_dict[key]]                
    params =  '?%s' % next_query_dict.urlencode() if next_query_dict else ''
    q['next'] = '%s%s' % (next_url, params)            
    return q.urlencode()

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