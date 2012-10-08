from selectable.base import ModelLookup
from estatebase.models import Street, Locality, Microdistrict, EstateType,\
    Estate, Region, EstateStatus, WallConstrucion, Origin, Beside, Interior,\
    Electricity, Watersupply, Gassupply, Sewerage, Driveway, Client, Contact,\
    ExUser, ClientType, Bid, EstateRegister, EstateTypeCategory
from selectable.registry import registry
from selectable.exceptions import LookupAlreadyRegistered

class SimpleIdLookup(ModelLookup):
    search_fields = ('id__icontains',)
    def get_item_label(self, item):
        if hasattr(item,'name'):            
            return u"%s, %s" % (item.pk, getattr(item,'name'))
        else:
            return u"%s" % item.pk        
    def get_item_value(self, item):
        return u"%s" % (item.pk,)

class ClientIdLookup(SimpleIdLookup):
    model = Client

class EstateRegisterIdLookup(SimpleIdLookup):
    model = EstateRegister    

class BidIdLookup(SimpleIdLookup):
    model = Bid

class SimpleNameLookup(ModelLookup):
    search_fields = ('name__icontains',)
    
class EstateLookup(ModelLookup):
    model = Estate
    search_fields = ('id__icontains',)
    def get_query(self, request, term):
        results = super(EstateLookup, self).get_query(request, term)        
        if request.user:
            results = results.filter(region__geo_group__userprofile__user__exact = request.user)
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

class EstateTypeCategoryLookup(SimpleNameLookup):
    model = EstateTypeCategory

class EstateTypeLookup(SimpleNameLookup):   
    model = EstateType 
    def get_query(self, request, term):
        results = super(EstateTypeLookup, self).get_query(request, term)
        results = results.filter(estate_type_category__independent = True)        
        self.category = request.GET.get('category', '')        
        if self.category:
            results = results.filter(estate_type_category_id = self.category)
        return results
    def get_item_label(self, item):
        if self.category:
            return u"%s" % (item.name)
        return u"%s, %s" % (item.name, item.estate_type_category or '')

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

class ClientTypeLookup(SimpleNameLookup):
    model = ClientType    
    
class ContactLookup(ModelLookup):
    model = Contact
    search_fields = ('contact__icontains',)

class ExUserLookup(ModelLookup):
    model = ExUser
    search_fields = ('username__icontains', 'first_name__icontains', 'last_name__icontains', 'email__icontains')
    
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
    registry.register(ExUserLookup)
    registry.register(ClientIdLookup)
    registry.register(ClientTypeLookup)
    registry.register(BidIdLookup)
    registry.register(EstateRegisterIdLookup)
    registry.register(EstateTypeCategoryLookup)
except LookupAlreadyRegistered:
    pass    
