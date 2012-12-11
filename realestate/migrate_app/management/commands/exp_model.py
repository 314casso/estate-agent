# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Electricity, Gassupply, Interior, WallConstrucion,\
    Watersupply, Telephony, Driveway, Sewerage, LandType, EstateType, Internet,\
    Heating, ExteriorFinish, Roof, WindowType, Flooring, WallFinish, Shape,\
    Ceiling, EstateStatus

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.print_model()        
    
    def print_model(self):
        template = u"u'%s': %s,"
        items = EstateStatus.objects.all()
        for item in items:
            print template % (item.name.lower(), item.pk)              
