# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Client


class Command(BaseCommand):    
    def handle(self, *args, **options):
        self.apply_checkbox()
        
    def apply_checkbox(self):
        STROITEL = 8
        CHASTNOE = 3
        q  = Client.all_objects.filter(client_type_id=STROITEL)
        for client in q:
            print u'Processing %s' % client 
            client.client_type_id = CHASTNOE
            client.has_dev_profile = True
            client.save()
    