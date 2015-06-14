# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Estate
from django.utils import translation


class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate('ru')   
        self.get_valid()      
                
    def get_valid(self):
        f = open('/tmp/post_ids.txt','w')
        post_ids = set(Estate.objects.filter(validity__exact=Estate.VALID).values_list('wp_meta__post_id', flat=True))
        for post_id in post_ids:
            f.write('%s\n' % post_id)
        f.close()