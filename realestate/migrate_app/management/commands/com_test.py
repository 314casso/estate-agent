# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from migrate_app.prop_map import PropMap
import os
from settings import MEDIA_ROOT
from django.db.models.aggregates import Count
from estatebase.models import Estate

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.test_func()        
    
    def test_func(self):    
        estates = Estate.objects.annotate(num_bidgs=Count('bidgs')).filter(num_bidgs__gt=1)        
        estates.delete()            
                      
        
          
            

        
