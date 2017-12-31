# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate, Microdistrict
from django.db.models.signals import post_save

class Command(BaseCommand):    
    def handle(self, *args, **options):
        self.actualize()
            
    def actualize(self):
        q = Estate.objects.all()        
        for estate in q:            
            Estate.objects.filter(pk=estate.pk).update(actualized=estate.get_actual_date())
            
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
    
