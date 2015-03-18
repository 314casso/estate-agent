import autocomplete_light
from models import Gear
from estatebase.models import Region, Locality

# This will generate a PersonAutocomplete class

class LocalityAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^name',]
    attrs = {        
        'data-autocomplete-minimum-characters': 1,
    }  
 
autocomplete_light.register(Locality, LocalityAutocomplete)

autocomplete_light.register(Gear,
    # Just like in ModelAdmin.search_fields
    search_fields=['^name',],
    attrs={        
        'data-autocomplete-minimum-characters': 1,
    },
    widget_attrs={
        #'data-widget-maximum-values': 3,
        # Enable modern-style widget !
        #'class': 'modern-style',
    },
)

autocomplete_light.register(Region,
    # Just like in ModelAdmin.search_fields
    search_fields=['^name',],
    attrs={
        # This will set the input placeholder attribute:
        #'placeholder': 'Other model name ?',
        # This will set the yourlabs.Autocomplete.minimumCharacters
        # options, the naming conversion is handled by jQuery
        'data-autocomplete-minimum-characters': 0,
    },
    # This will set the data-widget-maximum-values attribute on the
    # widget container element, and will be set to
    # yourlabs.Widget.maximumValues (jQuery handles the naming
    # conversion).
    widget_attrs={
        #'data-widget-maximum-values': 3,
        # Enable modern-style widget !
        #'class': 'modern-style',
    },
    autocomplete_js_attributes={'placeholder': 'region name ..'}
)