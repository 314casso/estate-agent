# -*- coding: utf-8 -*-
def join_strings(strings, delim=''):
    result = [x.strip() for x in strings if x.strip()]
    return delim.join(result)
    