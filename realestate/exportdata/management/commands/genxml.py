# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from optparse import make_option
from exportdata.models import BaseFeed
import os
from settings import MEDIA_ROOT
from django.utils import translation
from exportdata.mappers.services import FeedEngineFactory


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--nocache',
            action='store_true',
            dest='nocache',
            default=False,
            help='Do not use cache'),                                             
        )
          
    def handle(self, *args, **options):       
        translation.activate('ru')
        use_cache = not options['nocache']
        f = {'active': True}
        if len(args) > 0:               
            f['name'] = args[0]                        
        for feed in BaseFeed.objects.filter(**f):         
            feed_engine = FeedEngineFactory.get_feed_engine(feed)                                     
            file_name = os.path.join(MEDIA_ROOT, 'feed' ,'%s.xml' % feed.name)                     
            feed_engine.gen_XML(feed.get_queryset(), file_name, use_cache)
                                
        