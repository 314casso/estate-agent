# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from lxml import etree
from estatebase.models import Locality
from exportdata.models import FeedLocality


class Command(BaseCommand):
    def handle(self, *args, **options):
        tree = etree.parse("exportdata/xml/Locations.xml")
        node = tree.xpath("/Locations/Region[@Id=632660]")
        FeedLocality.objects.all().delete()
        for locality  in Locality.objects.all():
            self.find_location(node[0], locality)  
            
#         print  etree.tostring(tree.getroot(),encoding='UTF-8')
        
#         for location in node[0]:
#             print location.get("Name")
        
    def find_location(self, node, locality):
        print u"finding... %s" % locality
        location = node.xpath(u"Location[@Name='%s']" % locality.name)
        if len(location) == 1:
            feed_locality = FeedLocality()
            feed_locality.feed_name = 'avito' 
            feed_locality.feed_code = location[0].get("Id")
            feed_locality.locality = locality
            feed_locality.save()
            
            
        
    
        