# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate, EntranceEstate

class Command(BaseCommand):    
    def handle(self, *args, **options):
        self.do_job()
        
    def do_job(self):        
        q = Estate.objects.filter(entrances__isnull=True)
        q = q.exclude(beside__isnull=True)
        for e in q:            
            EntranceEstate.objects.create(estate=e,type=1,basic=True,beside=e.beside)
