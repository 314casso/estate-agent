# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from migrate_app.prop_map import PropMap

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.test_func()        
    
    def test_func(self):
        prop_map = PropMap()
        prop_map.test_param()              
