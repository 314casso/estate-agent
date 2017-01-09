# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate, Microdistrict

class Command(BaseCommand):    
    def handle(self, *args, **options):
        self.do_job()
        
    def do_job(self):        
#         estate_number=u'0',
        q = Estate.objects.filter(microdistrict__name__startswith=u'неправ')
        print len(q)
        for item in q:
            try:
                m = Microdistrict.objects.get(name=u'жилой район', locality=item.locality)
#                 print m 
            except:
                print  item.locality
#             print item         
#             item.street = None 
#             item.estate_number = None
#             item.address_state = Estate.NO_NUMBER
#             item.save()
