from django.http import QueryDict
import re
from decimal import Decimal

def safe_next_link(full_path):
    q = QueryDict('', mutable=True)        
    q['next'] = full_path
    return q.urlencode(safe='/')

def parse_decimal(value, splitter=None, index=1):    
    value = re.sub(r'[^\d,.-/]', '', value)
    value = value.replace(',','.')
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
              
                          
#print parse_decimal('2/500', splitter='/', index=0)        