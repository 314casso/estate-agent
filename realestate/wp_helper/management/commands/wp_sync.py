# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from wp_helper.service import WPService
from settings import WP_PARAMS
from estatebase.models import Estate
from django.utils import translation
from wp_helper.models import EstateWordpressMeta
from django.core.cache import cache
import time
import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate('ru')        
        wp_service = WPService(WP_PARAMS['site'])
        self.sync_correct(wp_service)      

    def sync_correct(self, wp_service):        
        TIME_TO_SLEEP = 3
        MAX_ERRORS = 5
        CACHE_TIME = 60 * 15
        SYNC_CACHE_KEY = 'SYNC_CORRECT'
        sync_cache_mark = cache.get(SYNC_CACHE_KEY)        
        if sync_cache_mark:
            return
        cache.set(SYNC_CACHE_KEY, datetime.datetime.now(), CACHE_TIME)
        estates = Estate.objects.filter(wp_meta__status=EstateWordpressMeta.XMLRPC)[:9]        
        total_errors = 0
        for estate in estates:                        
            if not wp_service.sync_post(estate):
                total_errors += 1
            if total_errors > MAX_ERRORS:
                break            
            time.sleep(TIME_TO_SLEEP)
        cache.delete(SYNC_CACHE_KEY)