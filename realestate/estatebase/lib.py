import re

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