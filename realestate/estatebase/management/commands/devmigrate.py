# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate

class Command(BaseCommand):    
    def handle(self, *args, **options):
        self.do_job()
        
    def do_job(self):        
#         estate_number=u'0',
        q = Estate.objects.filter(estate_number=u'0', address_state__isnull=True)
        print len(q)
        for item in q:            
#             item.street = None 
            item.estate_number = None
            item.address_state = Estate.NO_NUMBER
            item.save()
