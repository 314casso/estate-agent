from estatebase.lookups import SimpleNameLookup
from wp_helper.models import WordpressMeta
from selectable.exceptions import LookupAlreadyRegistered
from selectable.registry import registry

class WordpressLocalityLookup(SimpleNameLookup):
    model = WordpressMeta

try:
    registry.register(WordpressLocalityLookup) 
except LookupAlreadyRegistered:
    pass   