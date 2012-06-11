from selectable.base import ModelLookup
from estatebase.models import Street, Locality, Microdistrict
from selectable.registry import registry
from selectable.exceptions import LookupAlreadyRegistered


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

class MicrodistrictLookup(StreetLookup):
    model = Microdistrict

try:
    registry.register(StreetLookup)
    registry.register(LocalityLookup)
    registry.register(MicrodistrictLookup)
except LookupAlreadyRegistered:
    pass    
