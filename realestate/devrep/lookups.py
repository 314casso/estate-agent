from estatebase.lookups import SimpleNameLookup, SimpleIdLookup
from devrep.models import PartnerType, WorkType, Gear, Quality, Experience,\
    Partner, Citizenship
from selectable.exceptions import LookupAlreadyRegistered
from selectable.registry import registry
from selectable.base import ModelLookup

class PartnerTypeLookup(SimpleNameLookup):
    model = PartnerType

class PartnerIdLookup(SimpleIdLookup):
    model = Partner

class GearLookup(SimpleNameLookup):
    model = Gear
    
class QualityLookup(SimpleNameLookup):
    model = Quality    

class ExperienceLookup(SimpleNameLookup):
    model = Experience
    
class PartnerLookup(SimpleNameLookup):
    model = Partner    
    
class CitizenshipLookup(SimpleNameLookup):
    model = Citizenship
    
class WorkTypeLookup(ModelLookup):
    model = WorkType  
    search_fields = ('name__icontains',)
    def get_query(self, request, term):
        results = super(WorkTypeLookup, self).get_query(request, term)       
        results = results.exclude(parent=None)
        return results
    def get_item_label(self, item):
        return u"%s, %s" % (item, item.parent)
    
try:
    registry.register(PartnerTypeLookup)  
    registry.register(WorkTypeLookup)
    registry.register(GearLookup)
    registry.register(QualityLookup)
    registry.register(ExperienceLookup)
    registry.register(PartnerLookup)
    registry.register(CitizenshipLookup)
    registry.register(PartnerIdLookup)
except LookupAlreadyRegistered:
    pass      