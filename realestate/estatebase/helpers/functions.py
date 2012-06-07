from django.http import QueryDict

def safe_next_link(full_path):
    q = QueryDict('', mutable=True)        
    q['next'] = full_path
    return q.urlencode(safe='/')

