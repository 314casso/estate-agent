# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from exportdata.custom_makers.yaxml import YandexXML
from optparse import make_option
import pinject
from exportdata.custom_makers.domexxml import DomexXML
from exportdata.custom_makers.cianxml import CianFlatsXML, CianCommerceXML
from exportdata.custom_makers.avitoxml import AvitoXML
from exportdata.custom_makers.bnxml import BnXML
from exportdata.custom_makers.avitopayxml import AvitoXMLPay
from exportdata.custom_makers.restate import Restate, IrrXML, NersXML,\
    GdeetotdomXML
from exportdata.custom_makers.yaxmlplusphoto import YaPlusPhoto
from exportdata.custom_makers.nndvxml import NndvXML
from exportdata.custom_makers.mlsnxml import MlsnXML
from exportdata.custom_makers.idinaidixml import IdinaidiXML

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
                   CianCommerceXML.name : CianCommerceXML,
                   AvitoXML.name : AvitoXML,
                   BnXML.name : BnXML,
                   AvitoXMLPay.name: AvitoXMLPay, 
                   Restate.name: Restate,
                   YaPlusPhoto.name: YaPlusPhoto,
                   NndvXML.name: NndvXML, 
                   MlsnXML.name: MlsnXML,
                   IdinaidiXML.name: IdinaidiXML,
                   IrrXML.name: IrrXML,
                   NersXML.name: NersXML,
                   GdeetotdomXML.name: GdeetotdomXML,  
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
        

