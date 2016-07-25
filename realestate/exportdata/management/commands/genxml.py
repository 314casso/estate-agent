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
        if len(args) == 0:
            print "Error! Please provide feed name in the first argument!"
            return
        translation.activate('ru')
        use_cache = not options['nocache']               
        feed_name = args[0]                
        feed = BaseFeed.objects.get(name=feed_name)        
        feed_engine = FeedEngineFactory.get_feed_engine(feed)                          
        file_name = os.path.join(MEDIA_ROOT, 'feed' ,'%s.xml' % feed_name)         
        feed_engine.gen_XML(feed.get_queryset(), file_name, use_cache)                    
        