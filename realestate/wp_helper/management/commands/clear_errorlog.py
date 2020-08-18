# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from wp_helper.models import EstateWordpressMeta
from estatebase.models import Estate

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.set_log()
                             
    def clear_log(self):
        error_qs = Estate.objects.filter(wp_meta__status=EstateWordpressMeta.ERROR)
        for estate in error_qs:
            estate.wp_meta.status = EstateWordpressMeta.OUT
            estate.wp_meta.save()
            
    
    def set_log(self):
        qs = Estate.objects.filter(validity__exact=Estate.VALID, wp_meta__status=EstateWordpressMeta.UPTODATE).count()
        print qs        
#         for estate in qs:
#             estate.wp_meta.status = EstateWordpressMeta.XMLRPC
#             estate.wp_meta.save()