# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Bid
from estatebase.signals import update_geo

class Command(BaseCommand):
    def handle(self, *args, **options):
        for b in Bid.objects.all():
            update_geo(Bid, b)
