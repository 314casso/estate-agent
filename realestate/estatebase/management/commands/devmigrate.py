# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate

class Command(BaseCommand):    
    def handle(self, *args, **options):
        self.do_job()
        
    def do_job(self):        
#         EntranceEstate.objects.all().delete()
        q = Estate.objects.filter(street__name=u'не присвоено', estate_number=u'0', address_state__isnull=True)
#         q = q.exclude(beside__isnull=True)
        for e in q:            
            print e.id
