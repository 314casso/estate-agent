# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from wp_helper.service import WPService
from settings import WP_PARAMS
from estatebase.models import Estate, EstateStatus
from django.utils import translation
from wp_helper.models import EstateWordpressMeta
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate('ru')        
        wp_service = WPService(WP_PARAMS['site'])
        self.sync_sold_status(wp_service)      
                
    def sync_sold_status(self, wp_service):
        estates = Estate.objects.filter(id=177505)
        for estate in estates:
            print 'for'
            print(wp_service.sync_post(estate))
