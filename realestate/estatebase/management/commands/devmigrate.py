# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate


class Command(BaseCommand):    
    def handle(self, *args, **options):
        self.do_job()
        
    def do_job(self):
        q = Estate.objects.filter(estate_params__in=(16,))
        for e in q:
            e.estate_params.add(*[14,])           
    