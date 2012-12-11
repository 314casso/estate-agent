# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Electricity, Gassupply, Interior, WallConstrucion,\
    Watersupply, Telephony, Driveway, Sewerage, LandType, EstateType, Internet,\
    Heating, ExteriorFinish, Roof, WindowType, Flooring, WallFinish, Shape,\
    Ceiling, EstateStatus , Locality
from maxim_base.models import Place

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.make_mapper()
   
    def make_mapper(self):
        mapper = {}
        for locality in Place.objects.all():
            try:            
                mapper[int(locality.id)] = Locality.objects.get(name__iexact=locality.name).pk
            except:
                print locality.name, locality.id                                
        print mapper
        
    def print_model(self):
        template = u"u'%s': %s,"
        items = EstateStatus.objects.all()
        for item in items:
            print template % (item.name.lower(), item.pk)
            
                          
locality_mapper = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14, 15: 15, 16: 16, 17: 17, 18: 18, 19: 19, 20: 20, 21: 21, 22: 24, 23: 25, 24: 26, 25: 27, 28: 30, 29: 31, 30: 32, 31: 34, 32: 33, 33: 35, 34: 36, 35: 37, 36: 38, 37: 39, 38: 40, 39: 41, 40: 42, 41: 43, 42: 44, 43: 45, 44: 46, 45: 47, 46: 48, 47: 49, 48: 50, 49: 51, 50: 52, 51: 53, 52: 54, 53: 55, 55: 56, 56: 57, 57: 58, 58: 59, 59: 61, 60: 64, 61: 62, 62: 63, 63: 65, 64: 66, 65: 67, 66: 68, 67: 69, 68: 70, 69: 71, 70: 72, 71: 75, 72: 76, 73: 77, 74: 78, 75: 79, 76: 80, 77: 81, 78: 82, 79: 83, 80: 84, 81: 85, 82: 86, 83: 87, 84: 88, 85: 89, 86: 90, 87: 91, 88: 92, 89: 93, 90: 94, 91: 96, 92: 95, 93: 97, 94: 98, 95: 99, 96: 100, 97: 101, 98: 102, 99: 103, 100: 104, 101: 105, 102: 106, 103: 107, 104: 108, 105: 109, 106: 110, 107: 111, 108: 112, 109: 113, 110: 114, 111: 115, 112: 117, 114: 120, 115: 121, 116: 122, 117: 123, 118: 124, 119: 125, 120: 126, 121: 127, 122: 128, 123: 129, 124: 119, 125: 116, 126: 74, 127: 73, 130: 60, 131: 23, 132: 22}