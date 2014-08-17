# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

import re
from estatebase.models import Street, StreetType

class Command(BaseCommand):    
    def handle(self, *args, **options):
        #улица, переулок, проспект, проезд, шоссе, аллея, тупик, бульвар        
        q = Street.objects.filter(street_type=None)
        for street in q:
            for st in StreetType.objects.all().order_by('id'):
                PATTERN = ur'\b%s\b' % st.name
                name = parse_street(street.name, PATTERN)
                if name:                
                    street.name = name
                    street.street_type_id = st.id
                    street.save()
                    continue
        
        q = Street.objects.filter(street_type=None)
        for street in q:
            street.street_type_id = StreetType.ULITSA
            street.save()                                   
                
def parse_street(street, pattern):
    if not re.search(pattern, street, flags=re.I | re.U):
        return
    s =  re.sub(pattern, '', u'%s' % street , flags=re.I | re.U)
    s =  re.sub(r'\s{2,}', ' ', s , flags=re.I | re.U)
    return s.strip().capitalize()
    