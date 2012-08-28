from selectable.base import ModelLookup
from estatebase.models import Street, Locality, Microdistrict, EstateType,\
    Estate, Region, EstateStatus, WallConstrucion, Origin, Beside, Interior,\
    Electricity, Watersupply, Gassupply, Sewerage, Driveway, Client, Contact
from selectable.registry import registry
from selectable.exceptions import LookupAlreadyRegistered

class SimpleNameLookup(ModelLookup):
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
    
class RegionLookup(SimpleNameLookup):
    model = Region

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

class MicrodistrictLookup(StreetLookup):
    model = Microdistrict

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

class EstateTypeLookup(SimpleNameLookup):
    model = EstateType

class WallConstrucionLookup(SimpleNameLookup):
    model = WallConstrucion       

class OriginLookup(SimpleNameLookup):
    model = Origin    
    
class BesideLookup(SimpleNameLookup):
    model = Beside      

class InteriorLookup(SimpleNameLookup):
    model = Interior    
    
class ElectricityLookup(SimpleNameLookup):
    model = Electricity    

class WatersupplyLookup(SimpleNameLookup):
    model = Watersupply

class GassupplyLookup(SimpleNameLookup):
    model = Gassupply

class SewerageLookup(SimpleNameLookup):
    model = Sewerage

class DrivewayLookup(SimpleNameLookup):
    model = Driveway

class ClientLookup(SimpleNameLookup):
    model = Client
    
class ContactLookup(ModelLookup):
    model = Contact
    search_fields = ('contact__icontains',)
    
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
    registry.register(WatersupplyLookup)    
    registry.register(GassupplyLookup)
    registry.register(SewerageLookup)
    registry.register(DrivewayLookup)
    registry.register(ClientLookup)
    registry.register(ContactLookup)
except LookupAlreadyRegistered:
    pass    
