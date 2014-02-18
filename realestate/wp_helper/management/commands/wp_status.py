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
        sold_items = (EstateStatus.SOLD, EstateStatus.REMOVED)
        exclude_statuses = (EstateWordpressMeta.OUT, EstateWordpressMeta.UPTODATE)
        estates = Estate.objects.exclude(wp_meta__status__in=exclude_statuses)        
        estates = estates.filter(estate_status_id__in=sold_items)
        for estate in estates:
            time.sleep(10)            
            wp_service.sync_status(estate)