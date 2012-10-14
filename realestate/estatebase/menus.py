# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

class MenuItem(object):
    def __init__(self, name, url_name, css=None):
        self.name = name    
        self.url_name = url_name
        self.css = css
    @property    
    def url(self):
        return reverse(self.url_name)    

def create_menu():
    result = []
    result.append(MenuItem(u'Лоты','estate-list'))
    result.append(MenuItem(u'Заявки','bid-list'))
    result.append(MenuItem(u'Добавить лот','select_estate_type','ajax-dialog'))
    
    return result

menu_items = create_menu()         