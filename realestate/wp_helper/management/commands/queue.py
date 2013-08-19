# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import translation
from estatebase.models import Estate

class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate('ru')       
        estates = Estate.objects.filter(wp_meta__status=3)
        for estate in estates:            
            print(estate.id)                                 
                
        