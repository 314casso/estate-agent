# -*- coding: utf-8 -*-
from estatebase.models import HistoryMeta, Client, Contact, Estate, EstateStatus,\
    EstateClient, EstateType, Locality
import datetime
from django.db import transaction
from spyder_helper.models import SpiderMeta


class DotDict(dict):
    def __getattr__(self, attr):
        return self.get(attr)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

class SpiderData(object):
    _required = ['phone', 'locality_id', 'estate_type_id']
    def __init__(self, item_dict):
        self._meta = item_dict.get('meta')
        self._item = item_dict.get('item')
        self._bidg = item_dict.get('bidg')        
        self.meta = DotDict(self._meta) 
        self.item = DotDict(self._item)
        self.bidg = DotDict(self._bidg)
                
    def get_empty(self):        
        empty = []
        for key in self._required:
            if not self._item.get(key):
                empty.append(key)
        return empty
    
    def has_bidg(self):
        for value in self._bidg.itervalues():
            if value:
                return True
        return False    
            
class SpiderStoreService(object):
    USER_ID = 4 #Бузенкова     
    @transaction.commit_on_success
    def add_lot(self, item_dict):
        try:                
            result = {}            
            spider_data = SpiderData(item_dict)            
            empty = spider_data.get_empty()                    
            if len(empty):
                raise ValueError('Spider item has empty fields %s' % ', '.join(empty))                                 
            item = spider_data.item
            client = self._create_client(item.name, item.origin_id)        
            self._create_contact(item.phone, client.id)        
            e = self._create_estate(spider_data, client.id)
            self._create_spyder_meta(spider_data.meta, e)
            result['estate_id'] = e.id
            result['status'] = 1
        except Exception, e:            
            result['status'] = 0
            result['error_message'] = str(e)             
        return result
        
    def _create_client(self, name, origin_id):        
        CLIENT_TYPE_ID = 3 #Частное лицо        
        history = HistoryMeta()        
        history.created = datetime.datetime.now()                
        history.created_by_id = self.USER_ID                
        history.save()                
        client = Client.objects.create(history=history, name=name, 
                              client_type_id = CLIENT_TYPE_ID, 
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
    
    def _create_estate(self, spider_data, client_id):
        history = HistoryMeta()        
        history.created = datetime.datetime.now()                
        history.created_by_id = self.USER_ID           
        history.save()
        e = Estate()
        e.history = history           
        estate_type = EstateType.objects.get(pk=spider_data.item.estate_type_id)
        e.estate_category_id = estate_type.estate_type_category_id
        e._estate_type_id = estate_type.id
        e.origin_id = spider_data.item.origin_id               
        e.agency_price = spider_data.item.price_digit
        e.estate_status_id = EstateStatus.NEW                       
        e.description = spider_data.item.note
        e.region_id = Locality.objects.get(pk=spider_data.item.locality_id).region_id        
        e.locality_id = spider_data.item.locality_id                                              
        e.save() 
        if spider_data.has_bidg():
            bidg = e.basic_bidg
            for k,v in spider_data._bidg:
                if v:                 
                    setattr(bidg, k, v) 
            bidg.save() 
        EstateClient.objects.create(client_id=client_id,
                                estate_client_status_id=EstateClient.ESTATE_CLIENT_STATUS,
                                estate=e)
        return e
    
    def _create_spyder_meta(self, meta, e=None):        
        spider_meta, created = SpiderMeta.objects.get_or_create(spider=meta.spider, url=meta.url)  # @UnusedVariable
        spider_meta.status = SpiderMeta.PROCESSED    
        spider_meta.phone_guess = meta.phone_guess
        spider_meta.estate = e        
        spider_meta.full_url = meta.full_url
        spider_meta.save()
        return spider_meta   

