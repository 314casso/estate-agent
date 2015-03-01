from devrep.models import Partner
from django.forms.models import ModelForm
from selectable.forms.widgets import AutoComboboxSelectMultipleWidget,\
    AutoComboboxSelectWidget
from devrep.lookups import PartnerTypeLookup, GearLookup,\
    QualityLookup, ExperienceLookup, PartnerLookup
from estatebase.lookups import RegionLookup, LocalityLookup
from django.forms.widgets import Textarea

class PartnerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
        multi_fields = ('partner_types', 'coverage_regions', 'coverage_localities', 'gears')
        for multi_field in multi_fields:
            self.fields[multi_field].help_text = ''
        self.fields['name'].widget.attrs = {'class':'long-input'}
            
    class Meta:                
        model = Partner
        fields = ('name', 'partner_types', 'coverage_regions', 'coverage_localities',
                  'person_count', 'quality', 'experience', 'note', 'gears', 'parent',
                  )
        widgets = {
                   'partner_types':AutoComboboxSelectMultipleWidget(PartnerTypeLookup),
                   'coverage_regions':AutoComboboxSelectMultipleWidget(RegionLookup), 
                   'coverage_localities':AutoComboboxSelectMultipleWidget(LocalityLookup),                   
                   'gears':AutoComboboxSelectMultipleWidget(GearLookup),
                   'quality':AutoComboboxSelectWidget(QualityLookup),                                      
                   'experience':AutoComboboxSelectWidget(ExperienceLookup),
                   'parent':AutoComboboxSelectWidget(PartnerLookup),
                   'note': Textarea(attrs={'rows':'5'}),
                  }