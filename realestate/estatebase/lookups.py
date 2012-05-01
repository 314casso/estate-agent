from selectable.base import ModelLookup
from realestate.estatebase.models import Street
from selectable.registry import registry
from selectable.exceptions import LookupAlreadyRegistered

class StreetLookup(ModelLookup):
    model = Street
    search_fields = ('name__icontains', )
    def get_query(self, request, term):
        results = super(StreetLookup, self).get_query(request, term)
        locality = request.GET.get('locality', '')
        if locality:
            results = results.filter(locality=locality)
        return results

    def get_item_label(self, item):
        return u"%s, %s" % (item.name, item.locality)

try:
    registry.register(StreetLookup)
except LookupAlreadyRegistered:
    pass    
