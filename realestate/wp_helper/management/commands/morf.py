# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import translation
from wp_helper.service import WPService
from settings import WP_PARAMS
from estatebase.models import Region, Locality, Beside, EstateType

class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate('ru')
#         self.morf(2, Region.objects.all(), 'regular_name')        
#         self.morf(2, Locality.objects.all())
#         self.morf(6, Locality.objects.all())        
#         self.morf(2, Beside.objects.all())
#         self.morf(6, Beside.objects.all())
#         self.morf(4, EstateType.objects.all())
    
    def morf(self, case, qset, fld='name'):   
        wp_service = WPService(WP_PARAMS['site'])     
        cases = {
            1 : 'nomn', #    именительный    Кто? Что?    хомяк ест
            2 : 'gent', #    родительный    Кого? Чего?    у нас нет хомяка
            3 : 'datv', #    дательный    Кому? Чему?    сказать хомяку спасибо
            4 : 'accs', #    винительный    Кого? Что?    хомяк читает книгу
            5 : 'ablt', #    творительный    Кем? Чем?    зерно съедено хомяком
            6 : 'loct', #    предложный    О ком? О чём? и т.п.    хомяка несут в корзинке
        }       
        for q in qset:
            name = getattr(q, fld)
            attr = '%s_%s' % (fld, cases[case])
            setattr(q, attr, wp_service.inflect(name, case))
            q.save()
            
            
        
                           
                
        