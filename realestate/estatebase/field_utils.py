# -*- coding: utf-8 -*-
import re
'''
Для формирование поля от до по двум значениям
'''
def from_to_values(values, field_name):    
    f = {}    
    if values[0] and not values[1]:
        f['%s__gte' % field_name] = values[0]
    elif not values[0] and values[1]:
        f['%s__lte' % field_name] = values[1]
    elif values[0] and values[1]:
        f['%s__range' % field_name] = values             
    return f or None    

'''
Обработка составного поля
'''
def complex_field_parser(value, field_name):    
    if not value[0]:
        return None    
    f = {'%s__exact' % field_name : value[0]}    
    if value[1]:            
        num = from_to(value[1], '%s_distance' % field_name)
        if num:
            f.update(num)                    
    return f or None    

def split_string(value):                 
    return [x.strip() for x in value.split(',')]

'''
Для формирование поля от до
'''
def from_to(value, field_name=None):
    f = {}
    if not value:
        return None    
    a = ''.join(value.split())
    matchobjs = re.match(r"^(?P<oper>\>|\<)(?P<n>\d+)$", a)
    if matchobjs:         
        if matchobjs.group('oper') == '>':
            if field_name:
                f['%s__gte' % field_name] = matchobjs.group('n')
            else:
                f['min'] = matchobjs.group('n')
                f['max'] = None    
        else:
            if field_name:
                f['%s__lte' % field_name] = matchobjs.group('n')
            else:
                f['max'] = matchobjs.group('n')
                f['min'] = None    
    else:
        matchobjs = re.match(r"^(?P<n1>\d+)\-(?P<n2>\d+)$", a)
        if matchobjs:
            if field_name:
                f['%s__range' % field_name] = (matchobjs.group('n1'), matchobjs.group('n2'))
            else:
                f['min'] = matchobjs.group('n1')
                f['max'] = matchobjs.group('n2')                
        else:
            matchobjs = re.match(r"^(?P<n>\d+)$", a)
            if matchobjs:
                if field_name:
                    f['%s__exact' % field_name] = matchobjs.group('n')
                else:
                    f['min'] = f['max'] = matchobjs.group('n')                            
    return f or None    

def check_value_list(values):
    for value in values:
        if value:
            return True
    return False    

