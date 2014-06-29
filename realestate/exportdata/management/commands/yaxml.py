# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from exportdata.xml_makers import YandexXML

class Command(BaseCommand):
    def handle(self, *args, **options):
        feed = YandexXML()
        feed.gen_XML()
        