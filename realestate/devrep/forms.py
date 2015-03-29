from devrep.models import Partner, ClientPartner, Address
from django.forms.models import ModelForm
from selectable.forms.widgets import AutoComboboxSelectMultipleWidget,\
    AutoComboboxSelectWidget, AutoCompleteSelectWidget,\
    AutoCompleteSelectMultipleWidget
from devrep.lookups import PartnerTypeLookup, GearLookup,\
    QualityLookup, ExperienceLookup, PartnerLookup
from estatebase.lookups import RegionLookup, LocalityLookup, MicrodistrictLookup,\
    StreetLookup
from django.forms.widgets import Textarea

#'coverage_regions', 'coverage_localities'

class PartnerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
#         multi_fields = ('partner_types',)
#         for multi_field in multi_fields:
#             self.fields[multi_field].help_text = ''
        self.fields['name'].widget.attrs = {'class':'long-input'}
            
    class Meta:                
        model = Partner
        fields = ('name', 'partner_type', 'person_count', 'note', 'parent',)
        widgets = {
                    'partner_type':AutoComboboxSelectWidget(PartnerTypeLookup),
                    #'coverage_regions':AutoComboboxSelectMultipleWidget(RegionLookup), 
                    #'coverage_localities':AutoCompleteSelectMultipleWidget(LocalityLookup),                   
                    #'gears':AutoCompleteSelectMultipleWidget(GearLookup),
                    #'quality':AutoComboboxSelectWidget(QualityLookup),                                      
                    #'experience':AutoComboboxSelectWidget(ExperienceLookup),
                    'parent':AutoCompleteSelectWidget(PartnerLookup),
                    'note': Textarea(attrs={'rows':'5'}),
                  }
    
class ClientPartnerThroughUpdateForm(ModelForm):
    class Meta:
        model = ClientPartner 
        fields = ['partner_client_status']
        
class AddressForm(ModelForm):
    class Meta:
        model = Address
        widgets = {
                    'region':AutoComboboxSelectWidget(RegionLookup), 
                    'locality':AutoCompleteSelectWidget(LocalityLookup),                   
                    'microdistrict':AutoCompleteSelectWidget(MicrodistrictLookup),
                    'street':AutoCompleteSelectWidget(StreetLookup),
                  } 
        