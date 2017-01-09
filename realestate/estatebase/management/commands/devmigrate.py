# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate, Microdistrict

class Command(BaseCommand):    
    def handle(self, *args, **options):
        self.do_job()
        
    def do_job(self):        
#         estate_number=u'0',
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
#                 print m 
            except:
                print  item.locality
#             print item         
#             item.street = None 
#             item.estate_number = None
#             item.address_state = Estate.NO_NUMBER
#             item.save()
