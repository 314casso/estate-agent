# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from exportdata.xml_makers import YandexXML

class Command(BaseCommand):
    def handle(self, *args, **options):
        use_cache = not 'nocache' in args
        feed = YandexXML(use_cache)
        feed.gen_XML()
        