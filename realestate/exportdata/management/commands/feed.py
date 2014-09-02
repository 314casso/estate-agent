# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from exportdata.custom_makers.yaxml import YandexXML
from optparse import make_option
import pinject
from exportdata.custom_makers.domexxml import DomexXML
from exportdata.custom_makers.cianxml import CianFlatsXML

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--nocache',
            action='store_true',
            dest='nocache',
            default=False,
            help='Do not use cache'),                                             
        )
    
    def get_class_by_feedname(self, arg):
        mapper = {
                   YandexXML.name : YandexXML,
                   DomexXML.name : DomexXML,
                   CianFlatsXML.name : CianFlatsXML,
                 }
        if arg in mapper:
            return mapper[arg]
        return None
    
    def handle(self, *args, **options):
        if len(args) == 0:
            print "Error! Please provide feed name in the first argument!"
            return
        use_cache = not options['nocache']       
        obj_graph = pinject.new_object_graph()
        clazz = self.get_class_by_feedname(args[0])
        if clazz is not None:
            feed = obj_graph.provide(clazz)        
            feed.gen_XML(use_cache)
        else:
            print "Feed name '%s' is not found" % args[0]
        

