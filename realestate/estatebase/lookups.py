from selectable.base import ModelLookup
from estatebase.models import Street, Locality, Microdistrict, EstateType,\
    Estate, Region, EstateStatus, WallConstrucion, Origin, Beside, Interior,\
    Electricity
from selectable.registry import registry
from selectable.exceptions import LookupAlreadyRegistered



class EstateTypeLookup(ModelLookup):
    model = EstateType
    search_fields = ('name__icontains',)        
    
class EstateLookup(ModelLookup):
    model = Estate
    search_fields = ('id__icontains',)
    def get_query(self, request, term):
        results = super(EstateLookup, self).get_query(request, term)        
        if request.user:
            results = results.filter(locality__geo_group__userprofile__user__exact = request.user)
        return results        
    
class EstateStatusLookup(ModelLookup):
    model = EstateStatus
    search_fields = ('id__icontains',)    
    
class RegionLookup(ModelLookup):
    model = Region
    search_fields = ('name__icontains',)    

class StreetLookup(ModelLookup):
    model = Street
    search_fields = ('name__icontains',)
    def get_query(self, request, term):
        results = super(StreetLookup, self).get_query(request, term)
        locality = request.GET.get('locality', '')
        if locality:
            results = results.filter(locality=locality)
        return results
    def get_item_label(self, item):
        return u"%s, %s" % (item.name, item.locality)

class LocalityLookup(ModelLookup):
    model = Locality
    search_fields = ('name__icontains',)
    def get_query(self, request, term):
        results = super(LocalityLookup, self).get_query(request, term)
        region = request.GET.get('region', '')
        if region:
            results = results.filter(region=region)
        return results
    def get_item_label(self, item):
        return u"%s, %s" % (item.name, item.region or '')

class WallConstrucionLookup(ModelLookup):
    model = WallConstrucion
    search_fields = ('name__icontains',)   

class OriginLookup(ModelLookup):
    model = Origin
    search_fields = ('name__icontains',)
    
class BesideLookup(ModelLookup):
    model = Beside
    search_fields = ('name__icontains',)    

class InteriorLookup(ModelLookup):
    model = Interior
    search_fields = ('name__icontains',)
    
class ElectricityLookup(ModelLookup):
    model = Electricity
    search_fields = ('name__icontains',)

class MicrodistrictLookup(StreetLookup):
    model = Microdistrict

try:
    registry.register(StreetLookup)
    registry.register(LocalityLookup)
    registry.register(MicrodistrictLookup)
    registry.register(EstateTypeLookup)
    registry.register(EstateLookup)
    registry.register(RegionLookup)
    registry.register(EstateStatusLookup)   
    registry.register(WallConstrucionLookup) 
    registry.register(OriginLookup)   
    registry.register(BesideLookup)
    registry.register(InteriorLookup)
    registry.register(ElectricityLookup)
except LookupAlreadyRegistered:
    pass    
