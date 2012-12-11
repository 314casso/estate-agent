# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import sys
from maxim_base.models import Source, Users, Customers, Contacts
from migrate_app.models import SourceOrigin, UserUser
from estatebase.models import Origin, Client, HistoryMeta, Contact,\
    ContactHistory
from django.contrib.auth.models import User
import datetime
from django.db import transaction
import re

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
        imported = list(Client.objects.using('default').values_list('id', flat=True))
        customers = customers.exclude(pk__in=imported).distinct()        
        for customer in customers:
            with transaction.commit_on_success():            
                history = HistoryMeta()        
                history.created = customer.treatment_date or datetime.datetime.now()                
                history.created_by_id = UserUser.objects.get(pk=customer.creator_id).user_id                
                history.save()                
                Client.objects.create(id=customer.id, history=history, name=customer.name, client_type_id=3, 
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
            
    
                
        
        
            
    
             
