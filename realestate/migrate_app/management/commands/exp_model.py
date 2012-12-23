# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from estatebase.models import Electricity, Gassupply, Interior, WallConstrucion,\
    Watersupply, Telephony, Driveway, Sewerage, LandType, EstateType, Internet,\
    Heating, ExteriorFinish, Roof, WindowType, Flooring, WallFinish, Shape,\
    Ceiling, EstateStatus , Locality, Origin, Region as R 
from maxim_base.models import Place, Source, Users, Region, Types,\
    OrderProperties, Properties
from django.contrib.auth.models import User
from migrate_app.models import TypesEstateType

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.compare_prop()
        #self.make_mapper_estate_type()
        #self.make_mapper_origin()
        #self.make_mapper_locality()
        #self.make_mapper_user()
        #self.make_mapper_region()
   
    def compare_prop(self):
        o_prop = OrderProperties.objects.values_list('name', flat=True).distinct()
        prop = Properties.objects.values_list('name', flat=True).distinct()                    
        print ', '.join(["'%s'" % x for x in o_prop])
        
   
    def make_mapper_estate_type(self):
        mapper = {}
        for etype in Types.objects.all():
            try:            
                mapper[int(etype.id)] = TypesEstateType.objects.get(source_id=etype.pk).estate_type.pk
            except:
                print etype.name, etype.id                                
        print mapper
        
    def make_mapper_locality(self):
        mapper = {}
        for locality in Place.objects.exclude(id__in=[133,54]):
            try:            
                mapper[int(locality.id)] = Locality.objects.get(name__iexact=locality.name.strip()).pk
            except:
                print locality.name, locality.id                                
        print mapper
    
    def make_mapper_region(self):
        mapper = {}
        for region in Region.objects.all():
            try:            
                mapper[int(region.id)] = R.objects.get(name__iexact=region.name.strip()).pk
            except:
                print region.name, region.id                                
        print mapper
    
    def make_mapper_user(self):
        mapper = {}
        for user in Users.objects.all():
            try:            
                mapper[int(user.id)] = User.objects.get(username__exact=user.user).pk
            except:
                print user.name, user.id, user.user                                
        print mapper    
        
    def make_mapper_wallfinish(self):
        mapper = {}
        for wf in WallFinish.objects.all():
            try:            
                mapper[int(wf.id)] = WallFinish.objects.get(name__iexact=wf.name).pk
            except:
                print wf.name                                
        print mapper      
        
    def make_mapper_origin(self):
        mapper = {}
        for origin in Source.objects.all():
            try:            
                mapper[int(origin.id)] = Origin.objects.get(name__iexact=origin.name).pk
            except:
                print origin.name, origin.id                                
        print mapper
        
    def print_model(self):
        template = u"u'%s': %s,"
        items = EstateStatus.objects.all()
        for item in items:
            print template % (item.name.lower(), item.pk)
            
