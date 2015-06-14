# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate, EstateStatus
from django.utils import translation
from wp_helper.models import EstateWordpressMeta

class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate('ru')   
        self.get_valid()      
                
    def get_valid(self):        
        estates = Estate.objects.filter(validity__exact=Estate.VALID)       
        for estate in estates:                        
            try:
                wp_meta = estate.wp_meta
#                 print "pk: %s post_id: %s" % (estate.id, wp_meta.post_id)
            except EstateWordpressMeta.DoesNotExist:
                print "pk: %s post_id: %s" % (estate.id, None)
                
             
        print len(estates)
    
    