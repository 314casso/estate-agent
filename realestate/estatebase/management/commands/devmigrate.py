# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate, Microdistrict, Contact
from django.db.models.signals import post_save
import unicodecsv
import os
from settings import MEDIA_ROOT


class Command(BaseCommand):    
    def handle(self, *args, **options):
        self.correct_lots_export()
            
    def actualize(self):
        q = Estate.objects.all()        
        for estate in q:            
            Estate.objects.filter(pk=estate.pk).update(actualized=estate.get_actual_date())
            
    def do_job(self):      
        q = Estate.objects.filter(microdistrict__name__startswith=u'неправиль')
        print len(q)
        for item in q:
            if not item.locality:
                item.microdistrict = None
                item.save()
                continue            
            try:
                m = Microdistrict.objects.get(name=u'жилой район', locality=item.locality)
                item.microdistrict = m
                item.save() 
            except:
                print  item.locality


    def correct_lots_export(self):     
        estates = Estate.objects.filter(validity_id=Estate.VALID)
        file_name = os.path.join(MEDIA_ROOT, 'feed' ,'%s.csv' % 'correct_lots_contacts')
        with open(file_name, "w") as csvfile:
            writer = unicodecsv.writer(csvfile)
            writer.writerow(['estate_id',
            'name1','phone11','phone12','phone13','phone14','phone15','email11','email12','email13','email14','email15',
            'name2','phone21','phone22','phone23','phone24','phone25','email21','email22','email23','email24','email25',
            'name3','phone31','phone32','phone33','phone34','phone35','email31','email32','email33','email34','email35',
            'name4','phone41','phone42','phone43','phone44','phone45','email41','email42','email43','email44','email45',
            'name5','phone51','phone52','phone53','phone54','phone55','email51','email52','email53','email54','email55',
            ]
            )
            for estate in estates:
                row = []
                row.append(estate.pk)        
                for client in estate.clients.all()[:5]:
                    row.append(u'%s' % client.name)
                    phones = set()
                                            
                    for contact in client.contacts.filter(contact_type=Contact.PHONE, contact_state__in=[Contact.AVAILABLE, Contact.NOTCHECKED, Contact.NOTRESPONDED])[:5]:                  
                        phones.add(u'%s' % (contact.contact))                
                                        
                    phones = list(phones)
                    add_empty_cols(phones)                    
                    row.extend(phones)
                    
                    emails = set()
                    for contact in client.contacts.filter(contact_type=Contact.EMAIL, contact_state__in=[Contact.AVAILABLE, Contact.NOTCHECKED, Contact.NOTRESPONDED])[:5]:                  
                        emails.add(u'%s' % (contact.contact))                
                        
                    emails = list(emails)            
                    add_empty_cols(emails)
                    row.extend(emails)    
                          
                writer.writerow(row)
            

def add_empty_cols(lst):
    cols = 5 - len(lst)
    if cols > 0:
        for x in range(cols):
            lst.append('')  