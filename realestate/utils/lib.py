# -*- coding: utf-8 -*-
'''
Created on 21.04.2012

@author: picasso
'''
streets = """
Социалистическая
Осоавиахима
Ботылева
Павловская 
Гаражный переулок
"""

area = """
Конно-спортивный комплекс
Солнечный берег к/п 
Ключевой к/п
Южный склон
Вишневый сад СТ
Бобрукова Щель
"""

def split_string(value):                 
    return [x.strip() for x in value.split(',')]

def get_template(params):
    return '''INSERT IGNORE INTO `realtydb`.`{table}` (`{field}`) VALUES ('{value}');'''.format(**params)

def print_list(lst):
    for l in lst:
        value = l.strip()
        if value:
            params['value'] = value
            print get_template(params)

lst = streets.splitlines()
params = {'table':'street', 'field' : 'name'}

print_list(lst)

lst = area.splitlines()
params = {'table':'area', 'field' : 'name'}

print_list(lst)

    
