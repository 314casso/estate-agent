# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Bid, Contact
from estatebase.signals import update_geo
import re

class Command(BaseCommand):
    def handle(self, *args, **options):
        q = Contact.objects.filter(contact__iregex=r'\D', contact_type_id=1)
        cnt = 0        
        for contact in q:
            clean_contact = re.sub(r'\D', '', contact.contact)
            sq = Contact.objects.filter(contact=clean_contact)
            sq.exclude(id=contact.id)            
            if len(sq) > 0:
                cnt+=1
                print "*"*100
                print '|%s|%s|' % (contact.id, contact.contact)
                for dup_contact in sq:
                    print '|%s|%s|' % (dup_contact.id, dup_contact.contact)
                print "*"*100                
            else:
                contact.contact = clean_contact
                contact.save()
                
        print 'TOTAL: %s' % cnt
                
                                 
        
        
