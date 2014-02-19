# -*- coding: utf-8 -*-

from realty.local_settings import DJANGO_PATHES
import sys
sys.path.extend(DJANGO_PATHES)
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

def setup_django_env(path):
    import imp
    from django.core.management import setup_environ
    f, filename, desc = imp.find_module('settings', [path])
    project = imp.load_module('settings', f, filename, desc)     
    setup_environ(project)
setup_django_env(DJANGO_PATHES[0])

import datetime
from django.db import transaction
from estatebase.models import Estate, Contact, HistoryMeta, Client, EstateClient,\
    EstateStatus, EstateType

class RealtyPipeline(object):   
    USER_ID = 4 #Бузенкова 
    def process_item(self, item, spider):
        for phone in item['phone']:                
            if self.is_phone_exist(phone):
                return item
        estate_type = EstateType.objects.get(pk=item['estate_type'])
        if not estate_type:
            return item
        name = u''.join(item['name']) or u'неизвестно'
        result_desc = []
        if item['price']:
            result_desc.append(u''.join(item['price']))
        if item['link']:
            result_desc.append(u''.join(item['link']))                        
        result_desc.append(u' '.join(item['desc']))      
        result_desc_str = u'\n'.join(result_desc)
        price_digit = self.clean_price_digit(item['price_digit']) 
        with transaction.commit_on_success():                        
            client = self._create_client(name, spider.ORIGIN_ID)
            for phone in item['phone']:
                self._create_contact(phone, client.id)        
            self._create_estate(spider.ORIGIN_ID, price_digit, result_desc_str, client.id, estate_type, spider.REGION_ID)
        return item
    
    def clean_price_digit(self, item_price_digit):
        result = item_price_digit[0] if item_price_digit else 0        
        if 10000 <= result <= 100000000:
            return result
        return 0

    def is_phone_exist(self, phone):
        contacts = Contact.objects.filter(contact=phone, contact_type_id=Contact.PHONE)
        if contacts:
            return True
        return False
    
    def _create_client(self, name, origin_id):        
        LIENT_TYPE_ID = 3 #Частное лицо        
        history = HistoryMeta()        
        history.created = datetime.datetime.now()                
        history.created_by_id = self.USER_ID                
        history.save()                
        client = Client.objects.create(history=history, name=name, 
                              client_type_id = LIENT_TYPE_ID, 
                              origin_id=origin_id)
        return client
        
    def _create_contact(self, contact, client_id):
        CONTACT_STATE_ID = 5 #Не проверен
        CONTACT_TYPE_ID = 1 #Телефон
        c = Contact()
        c.migration = True
        c.user_id = self.USER_ID         
        c.client_id = client_id
        c.contact_type_id = CONTACT_TYPE_ID 
        c.contact = contact 
        c.updated = datetime.datetime.now() 
        c.contact_state_id = CONTACT_STATE_ID
        c.save()
        return c
    
    def _create_estate(self, origin_id, price_digit, description, client_id, estate_type, region_id):                                    
        history = HistoryMeta()        
        history.created = datetime.datetime.now()                
        history.created_by_id = self.USER_ID           
        history.save()
        e = Estate()
        e.history = history           
        e.estate_category_id = estate_type.estate_type_category_id
        e._estate_type_id = estate_type.id
        e.origin_id = origin_id               
        e.agency_price = price_digit
        e.estate_status_id = EstateStatus.NEW                       
        e.description = description
        e.region_id = region_id                                              
        e.save() 
        EstateClient.objects.create(client_id=client_id,
                                estate_client_status_id=EstateClient.ESTATE_CLIENT_STATUS,
                                estate=e)
            