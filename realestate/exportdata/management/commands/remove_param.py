# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate

class Command(BaseCommand):
    def handle(self, *args, **options):
        PARAM_IDs = [15,4,19,13,8,9,11,12,20]
        for PARAM_ID in PARAM_IDs: 
            q = Estate.objects.filter(estate_params__exact=PARAM_ID)
            for estate in q:
                estate.estate_params.remove(PARAM_ID)       
