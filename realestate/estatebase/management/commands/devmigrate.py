# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate

class Command(BaseCommand):    
    def handle(self, *args, **options):
        self.do_job()
        
    def do_job(self):        
        q = Estate.objects.filter(street__name=u'не присвоено', estate_number=u'0', address_state__isnull=True)
        for item in q:            
            item.street = None 
            item.estate_number = None
            item.address_state = Estate.NO_ADDRESS
            item.save()
