# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import sys
from maxim_base.models import Source, Users, Customers, Contacts, RealEstate,\
    Properties, Descriptions, Images, Orders, OrderProperties, Place
from migrate_app.models import SourceOrigin, UserUser, TypesEstateType,\
    BidImport
from estatebase.models import Origin, Client, HistoryMeta, Contact,\
    ContactHistory, Estate, Locality, Street, Microdistrict, EstateClient,\
    EstatePhoto, Bid
from django.contrib.auth.models import User
import datetime
from django.db import transaction
import re
from migrate_app.prop_map import PropMap
import os
from settings import MEDIA_ROOT
from migrate_app.order_prop_map import OrderPropMap

class Command(BaseCommand):
    args = '<function_name function_name ...>'
    help = 'Migrate date'

    def handle(self, *args, **options):
        for function_name in args:
            try:
                func = getattr(self, function_name)
                if callable(func):
                    func()
                else:
                    sys.stderr.write('%s is not callable' % function_name)
            except Exception, err:                
                raise CommandError('ERROR: %s\n' % str(err))
    def origin(self):
        imported = list(SourceOrigin.objects.using('default').values_list('source_id', flat=True))
        sources = Source.objects.using('maxim_db').exclude(pk__in=imported)
        for source in sources:
            origin = Origin.objects.using('default').get(name__exact=source.name)                        
            SourceOrigin.objects.using('default').create(source_id=source.pk, origin=origin)
        
    def user(self):
        imported = list(UserUser.objects.using('default').values_list('source_id', flat=True))
        sources = Users.objects.using('maxim_db').exclude(pk__in=imported)
        for source in sources:
            try:
                user = User.objects.using('default').get(username__exact=source.user)
            except User.DoesNotExist:
                user = User.objects.using('default').get(username__exact='migrated')
            UserUser.objects.using('default').create(user=user, source_id=source.pk)
        
    def client(self):        
        customers = Customers.objects.using('maxim_db').filter(contacts__id__isnull=False)
        imported = list(Client.all_objects.using('default').values_list('id', flat=True))
        customers = customers.exclude(pk__in=imported).distinct()        
        for customer in customers:
            with transaction.commit_on_success():            
                history = HistoryMeta()        
                history.created = customer.treatment_date or datetime.datetime.now()                
                history.created_by_id = UserUser.objects.get(pk=customer.creator_id).user_id                
                history.save()                
                Client.objects.create(id=customer.id, history=history, name=customer.name, 
                                      client_type_id=self.client_type_parser(customer.name) or 3, 
                                      origin_id=SourceOrigin.objects.get(pk=customer.source_id or 14).origin_id, 
                                      address=customer.from_where, note=customer.comments)
    
    def contact(self):
        contacts = Contacts.objects.using('maxim_db').all()
        imported = list(Contact.objects.values_list('id', flat=True))
        contacts = contacts.exclude(pk__in=imported).distinct()
        for contact in contacts:
            with transaction.commit_on_success():
                c = Contact()
                c.migration = True
                c.id = contact.id 
                c.client_id = contact.customer_id
                c.contact_type_id = self._contact_type(contact.contact) 
                c.contact = contact.contact 
                c.updated = contact.update_record or datetime.datetime.now() 
                c.contact_state_id = self._contact_state(contact.status)
                c.save()
        self.contact_history()                
    
    
    def estate_check(self):
        print self._get_region_id(2)
        
    def _get_region_id(self, value):
        mapper = {1: 1, 2: 3, 3: 2, 4: 4}                
        return mapper[value]        

    def get_locality(self, place_id, region_id, place_name):
        if place_id == 26: #Виноградный дублируется
            if region_id == 1:
                return Locality.objects.get(pk=28)
            elif region_id == 4:
                return Locality.objects.get(pk=29)
            else:
                return Locality.objects.get(pk=27)                       
        else:
            try: 
                return Locality.objects.get(name__iexact=place_name)
            except Locality.DoesNotExist:
                return None
    
    def estate(self):        
        real_estates = RealEstate.objects.using('maxim_db').exclude(place_id__in=[133,54])
        imported = list(Estate.all_objects.values_list('id', flat=True))
        real_estates = real_estates.exclude(pk__in=imported).distinct()        
        for real_estate in real_estates: 
            if real_estate.type_id == 0:
                continue            
            if real_estate.status_id == 3 and real_estate.update_record < datetime.datetime(2011, 11, 1, 0, 0, 0):
                continue 
            clients_id = []
            for customer_id in real_estate.customers.values_list('customer_id', flat=True):
                try:
                    client = Client.objects.get(pk=customer_id)
                    clients_id.append(client.pk)
                except Client.DoesNotExist:                    
                    pass                
            if len(clients_id) == 0:                                                
                continue            
            with transaction.commit_on_success():
                print real_estate.pk                
                history = HistoryMeta()        
                history.created = real_estate.creation_date or datetime.datetime.now()                
                history.created_by_id = UserUser.objects.get(pk=real_estate.creator_id).user_id
                history.updated = real_estate.update_record
                history.updated_by_id = UserUser.objects.get(pk=real_estate.last_editor_id).user_id                 
                history.save()
                e = Estate()
                e.history = history
                estate_type_type = TypesEstateType.objects.get(source_id=real_estate.type_id)
                estate_type = estate_type_type.estate_type
                e.estate_category_id = estate_type.estate_type_category_id
                e._estate_type_id = estate_type.pk
                e.origin_id = SourceOrigin.objects.get(pk=real_estate.source_id or 14).origin_id               
                e.locality = self.get_locality(real_estate.place_id, real_estate.region_id, real_estate.place.name.strip())                                                 
                e.region_id = e.locality.region_id
                if real_estate.street_id and real_estate.street_id != 1:
                    street, created = Street.objects.get_or_create(name=real_estate.street.name.strip(), locality=e.locality) # @UnusedVariable
                    e.street = street                
                if real_estate.area_id and real_estate.area_id != 1:
                    microdistrict, created = Microdistrict.objects.get_or_create(name=real_estate.area.name.strip(), locality=e.locality) # @UnusedVariable
                    e.microdistrict = microdistrict
                e.estate_number = real_estate.house_number.strip()
                e.saler_price = real_estate.cost
                e.agency_price = real_estate.cost_markup
                e.estate_status_id = real_estate.status_id
                e.id = real_estate.pk       
                descriptions = Descriptions.objects.filter(real_estate=real_estate)
                dlist = []
                for description in descriptions:
                    d = description.description.strip()
                    if d:
                        dlist.append(d)                                     
                e.description = '; '.join(dlist)                              
                e.save()           
                prop_map = PropMap(e)                
                properties = Properties.objects.filter(real_estate=real_estate)                
                for prop in properties:                     
                    prop_map.set_param(prop)              
                if real_estate.type_id == 9:
                    prop_map.set_state(u'недостроено')
                if real_estate.type_id == 8:
                    prop_map.set_state(u'ветхое')                
                prop_map.save_params()          
                for client_id in clients_id:
                    EstateClient.objects.create(client_id=client_id,
                                        estate_client_status_id=EstateClient.ESTATE_CLIENT_STATUS,
                                        estate=e)
                for file_name in real_estate.images.values_list('file_name', flat=True):                                        
                    if os.path.isfile(os.path.join(MEDIA_ROOT, 'photos', str(e.pk), file_name)):
                        EstatePhoto.objects.create(estate=e, image=os.path.join('photos', str(e.pk), file_name))                  
                    
    
    def _contact_state(self, contact):
        mapper = {u'доступен':1,u'заблокирован':3,u'недоступен':2,u'нет ответа':4}
        if contact in mapper:
            return mapper[contact]
        return 5
   
    def _contact_type(self, contact):
        if self._validate_email(contact):
            return 2           
        if re.search(r"[^0-9\+\-\(\)]", contact):
            return 3
        else:
            return 1
   
    def _validate_email(self, email):
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False             

    def client_type_parser(self, name):
        '''
        Агенство 2
        Застройщик 4
        Нет агентам 5
        Ошибка 6
        Риелтор 1
        Частное лицо 3
        '''
        if re.search(ur"нет{0,1}\s*агент|нет{0,1}\s*сотруд|нет{0,1}\s*работ", name, flags=re.IGNORECASE | re.UNICODE):
            return 5
        if re.search(ur"агентство", name, flags=re.IGNORECASE | re.UNICODE):
            return 2
        if re.search(ur"агент|риэлтор|риелтор", name, flags=re.IGNORECASE | re.UNICODE):
            return 1
        if re.search(ur"не\s*прод", name, flags=re.IGNORECASE | re.UNICODE):
            return 6
        
    @transaction.commit_on_success
    def update_client_type(self):
        clients = Client.objects.all()
        for client in clients:      
            type_id = self.client_type_parser(client.name)
            if type_id:      
                client.client_type_id = type_id  
                client.save()
        
    @transaction.commit_on_success
    def contact_history(self):
        histories = ContactHistory.objects.filter(user_id__isnull=True)
        for h in histories:
            if not h.user_id:
                h.user_id = h.contact.client.history.created_by_id
                h.save()      
    
    def set_bid_status(self, value):
        pass
        #mapper = {'новая': ,'передана':, 'отказ': }

    def bid(self):
        orders = Orders.objects.using('maxim_db').all()
        
        imported = list(BidImport.objects.values_list('external_id', flat=True))
        orders = orders.exclude(pk__in=imported).distinct()
        for order in orders:
            with transaction.commit_on_success():
                if not Client.objects.filter(pk=order.customer_id):
                    continue                    
                history = HistoryMeta()        
                history.created = order.creation_date or datetime.datetime.now()                
                history.created_by_id = UserUser.objects.get(pk=order.creator_id).user_id
                history.updated = order.update_record
                history.updated_by_id = UserUser.objects.get(pk=order.last_editor_id).user_id                 
                history.save()
                bid = Bid()  
                external_id = None
                try:
                    Bid.objects.get(pk=order.id)                    
                except Bid.DoesNotExist:
                    external_id = order.id
                
                if external_id:  
                    bid.id = external_id
                                    
                bid.client_id = order.customer_id 
                bid.history = history
                
                bid.save()
                
                prop_map = OrderPropMap(bid)               
                
                prop_map._set_types(order.types.values_list('type_id',flat=True))                
                regions = list(order.regions.values_list('region_id', flat=True))
                first_region = regions[0] if len(regions) else None
                clean_localities = []
                clean_regions = [self._get_region_id(pk) for pk in regions]
                               
                for place_id in order.places.values_list('place_id', flat=True):
                    locality = self.get_locality(place_id, first_region, Place.objects.get(pk=place_id).name)
                    if locality:
                        clean_localities.append(locality)
                if len(clean_localities):   
                    prop_map.pickle_dict['locality'] = clean_localities
                else:
                    prop_map.pickle_dict['region'] = clean_regions
                if order.cost_from or order.cost_to:
                    prop_map.pickle_dict['agency_price'] = [order.cost_from, order.cost_to]     
                
                properties = OrderProperties.objects.filter(order=order)                
                for prop in properties:                     
                    prop_map.set_param(prop)
                
                clean_users = []
                for user_id in order.users.values_list('user_id', flat=True):
                    clean_users.append(UserUser.objects.get(pk=user_id).user_id)
                
                if len(clean_users):
                    bid.brokers = clean_users

                #print prop_map.pickle_dict
                bid.cleaned_filter = prop_map.pickle_dict
                bid.bid_status = [9]
                bid.save()
                BidImport.objects.create(external_id=order.id, bid=bid)
