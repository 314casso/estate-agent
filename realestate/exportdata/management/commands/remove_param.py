# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate

class Command(BaseCommand):
    def handle(self, *args, **options):
        PARAM_ID = 4
        q = Estate.objects.filter(estate_params__exact=PARAM_ID)
        for estate in q:
            estate.estate_params.remove(PARAM_ID)       
