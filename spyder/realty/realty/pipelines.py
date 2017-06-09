# -*- coding: utf-8 -*-
import datetime
from django.db import transaction
from estatebase.models import Estate, Contact, HistoryMeta, Client, EstateClient,\
    EstateStatus, EstateType
from spyder_helper.models import SpiderMeta
from realty.utils import get_url_path

class RealtyPipeline(object):   
    USER_ID = 4 #Бузенкова
    @transaction.atomic() 
    def process_item(self, item, spider):
        print 'processing... %s' % item['link'] 
        if 'do_not_process' in item and item['do_not_process']:
            print 'Do not process...' 
            self._create_spyder_meta(spider.name, item, SpiderMeta.DO_NOT_PROCESS)
            return item            
        if 'phone' not in item or not item['phone'] or not item['phone'][0]:
            self._create_spyder_meta(spider.name, item, SpiderMeta.NOPHONE)
            return item
        for phone in item['phone']:                
            if self.is_phone_exist(phone):
                self._create_spyder_meta(spider.name, item, SpiderMeta.EXISTSPHONE)
                return item
        estate_type = EstateType.objects.get(pk=item['estate_type_id'])
        if not estate_type:
            return item
        name = u''.join(item['name']) or u'неизвестно'       
        client = self._create_client(name, spider.ORIGIN_ID)
        for phone in item['phone']:
            self._create_contact(phone, client.id)        
        e = self._create_estate(item, spider.ORIGIN_ID, client.id, estate_type)
        self._create_spyder_meta(spider.name, item, SpiderMeta.PROCESSED, e)
        return item
    
    def clean_price_digit(self, item_price_digit):
        result = item_price_digit[0] if item_price_digit else 0        
        if 10000 <= result <= 100000000:
            return result
        return 0

    def is_phone_exist(self, phone):
        print "CHECK PHONE %s" % phone 
        if phone:
            contacts = Contact.objects.filter(contact=phone, contact_type_id=Contact.PHONE)
            if contacts:
                return True
        return False
    
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
    
    def _create_estate(self, item, origin_id, client_id, estate_type):
        history = HistoryMeta()        
        history.created = datetime.datetime.now()                
        history.created_by_id = self.USER_ID           
        history.save()
        e = Estate()
        e.history = history           
        e.estate_category_id = estate_type.estate_type_category_id
        e._estate_type_id = estate_type.id
        e.origin_id = origin_id               
        e.agency_price = self.clean_price_digit(item['price_digit'])
        e.estate_status_id = EstateStatus.NEW                       
        e.description = self.get_description(item)
        e.region_id = item['region_id']
        if 'locality_id' in item:
            e.locality_id = item['locality_id']                                              
        e.save() 
        if item.has_extra_bidg():
            bidg = e.basic_bidg
            for field in item.BIDG_FIELDS:                 
                if field in item:                                    
                    setattr(bidg, field, item[field]) 
            bidg.save() 
        EstateClient.objects.create(client_id=client_id,
                                estate_client_status_id=EstateClient.ESTATE_CLIENT_STATUS,
                                estate=e)
        return e
    
    def get_description(self, item):
        result_desc = []
        if item['price']:
            result_desc.append(u''.join(item['price']))
        if item['link']:
            result_desc.append(u''.join(item['link']))                        
        result_desc.append(u' '.join(item['desc']))      
        return u'\n'.join(result_desc)
    
    def _create_spyder_meta(self, spider, item, status, e=None):        
        spider_meta, created = SpiderMeta.objects.get_or_create(spider=spider, url=get_url_path(item['link']))  # @UnusedVariable
        spider_meta.status = status
        if item['phone']:
            spider_meta.phone = item['phone'][0]
        spider_meta.phone_filename = item.get('phone_filename')
        spider_meta.phone_guess = item.get('phone_guess')
        spider_meta.estate = e
        url = item['link']
        spider_meta.full_url = url if isinstance(url, basestring) else url[0]
        spider_meta.save()
        return spider_meta
            