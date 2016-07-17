# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from lxml import etree
from estatebase.models import Locality
from exportdata.models import ValueMapper, MappedNode
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    _mapped_node = None
    _debug = False

    @property
    def mapped_node(self):
        if not self._mapped_node:
            self._mapped_node = MappedNode.objects.get(xml_node='City')
        return self._mapped_node
        
    def handle(self, *args, **options):
        tree = etree.parse("http://autoload.avito.ru/format/Locations.xml")
        node = tree.xpath("/Locations/Region[@Id=632660]")
        q = ValueMapper.objects.filter(content_type=ContentType.objects.get_for_model(Locality), mapped_node=self.mapped_node)
        q.delete()
        for locality  in Locality.objects.all():
            self.find_location(node[0], locality)
        if self._debug: 
            print  etree.tostring(tree.getroot(),encoding='UTF-8')          
            for location in node[0]:
                print location.get("Name")
        
    def find_location(self, node, locality):        
        location = node.xpath(u"City[@Name='%s']" % locality.name)        
        if len(location) == 1:
            ValueMapper.objects.create(content_object=locality, mapped_node=self.mapped_node, xml_value=locality.name)            
            
            
        
    
        