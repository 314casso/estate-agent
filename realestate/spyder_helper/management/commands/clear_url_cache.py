# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from spyder_helper.models import SpiderMeta

class Command(BaseCommand):
    def handle(self, *args, **options):
        SpiderMeta.objects.all().delete()
        