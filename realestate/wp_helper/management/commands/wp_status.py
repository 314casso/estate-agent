# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from wp_helper.service import WPService
from settings import WP_PARAMS
from estatebase.models import Estate, EstateStatus
from django.utils import translation

class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate('ru')        
        wp_service = WPService(WP_PARAMS['site'])
        self.sync_sold_status(wp_service)      
                
    def sync_sold_status(self, wp_service):
        sold_items = (EstateStatus.SOLD, EstateStatus.REMOVED)
        estates = Estate.objects.exclude(wp_meta__status=3)        
        estates = estates.filter(estate_status_id__in=sold_items)
        for estate in estates:            
            wp_service.sync_status(estate)