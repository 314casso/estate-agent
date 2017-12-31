import re
from django.utils import timezone
from settings import CORRECT_DELTA, FREE_DELTA
from django.core.cache import cache

def first_last(iterable):
    i = iter(iterable)
    f = next(i)
    yield f, "first"
    n = next(i)
    for another in i:
        yield n, None
        n = another
    yield n, "last"

def format_phone(phone_number):
    pattern = r'^8'
    repl = '+7'
    result = phone_number
    if len(phone_number) > 9:
        result =  re.sub(pattern, repl, phone_number , re.I | re.U)
    return result

def get_delta(key, delta_days):    
    delta = cache.get(key)
    if not delta:
        delta = timezone.now() - delta_days
        cache.set(key, delta, 60)        
    return delta

def get_validity_delta():
    return get_delta('validity_delta', CORRECT_DELTA)    

def get_free_delta():
    return get_delta('outdated_delta', FREE_DELTA)
    
    