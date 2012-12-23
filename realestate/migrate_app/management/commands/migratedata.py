# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import sys
from maxim_base.models import Source, Users, Customers, Contacts, RealEstate,\
    Properties, Descriptions, Images, Orders
from migrate_app.models import SourceOrigin, UserUser, TypesEstateType
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
                locality = None
                if real_estate.place_id == 26: #Виноградный дублируется
                    if real_estate.region_id == 1:
                        locality = Locality.objects.get(pk=28)
                    elif real_estate.region_id == 4:
                        locality = Locality.objects.get(pk=29)
                    else:
                        locality = Locality.objects.get(pk=27)                       
                else:
                    locality = Locality.objects.get(name__iexact=real_estate.place.name.strip())
                e.locality = locality                                                 
                e.region_id = locality.region_id
                if real_estate.street_id and real_estate.street_id != 1:
                    street, created = Street.objects.get_or_create(name=real_estate.street.name.strip(), locality=locality) # @UnusedVariable
                    e.street = street                
                if real_estate.area_id and real_estate.area_id != 1:
                    microdistrict, created = Microdistrict.objects.get_or_create(name=real_estate.area.name.strip(), locality=locality) # @UnusedVariable
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
        imported = list(Bid.objects.values_list('id', flat=True))
        orders = orders.exclude(pk__in=imported).distinct()
        for order in orders:
            with transaction.commit_on_success():
                history = HistoryMeta()        
                history.created = order.creation_date or datetime.datetime.now()                
                history.created_by_id = UserUser.objects.get(pk=order.creator_id).user_id
                history.updated = order.update_record
                history.updated_by_id = UserUser.objects.get(pk=order.last_editor_id).user_id                 
                history.save()
                bid = Bid()
                bid.id = order.id
                bid.history = history
                                   
        
                
#    Кол заявки, Дата создания, создатель, Коды, тип объекта, район, населенные пункты, цена, 
#дополнительное описание к внешнему описанию и участку в одно поле в новой базе.
#Остальные поля, если не затратно по времени и силам: 
#общ площадь, колво комнат, материал стен, площадь участка, год постройки Но не обязательно!

#customer = models.ForeignKey(Customers)

#    status = models.CharField(max_length=60)
#    cost_from = models.IntegerField(null=True, blank=True)
#    cost_to = models.IntegerField(null=True, blank=True)
#    operation = models.TextField(blank=True)
#    result = models.TextField(blank=True)            
    
                
        
        
            
    
             
