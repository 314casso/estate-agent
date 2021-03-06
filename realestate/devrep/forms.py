# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from devrep.models import Partner, ClientPartner, Address, DevProfile,\
    WorkTypeProfile, ExtraProfile, GoodsProfileM2M, Goods
from django.forms.models import ModelForm, BaseInlineFormSet,\
    inlineformset_factory
from selectable.forms.widgets import AutoComboboxSelectMultipleWidget,\
    AutoComboboxSelectWidget, AutoCompleteSelectWidget,\
    AutoCompleteSelectMultipleWidget
from devrep.lookups import PartnerTypeLookup, GearLookup,\
    QualityLookup, ExperienceLookup, PartnerLookup, PartnerIdLookup,\
    WorkTypeLookup, MeasureLookup, CitizenshipLookup, GoodsLookup
from estatebase.lookups import RegionLookup, LocalityLookup, MicrodistrictLookup,\
    StreetLookup, ExUserLookup
from django.forms.widgets import Textarea, DateTimeInput, TextInput
from django.core.exceptions import ValidationError
from django import forms
from selectable.forms.fields import AutoCompleteSelectMultipleField
from django.forms.forms import Form
from estatebase.field_utils import history_filter
from estatebase.fields import DateRangeField, LocalIntegerField
from django.db.models import Q


class PartnerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'class':'long-input'}
            
    class Meta:                
        model = Partner
        fields = ('name', 'partner_type', 'person_count', 'note', 'parent',)
        widgets = {
                    'partner_type':AutoComboboxSelectWidget(PartnerTypeLookup),                    
                    'parent':AutoCompleteSelectWidget(PartnerLookup),
                    'note': Textarea(attrs={'style':'height:150px; width:500px'}),
                  }
    
class ClientPartnerThroughUpdateForm(ModelForm):
    class Meta:
        model = ClientPartner 
        fields = ('partner_client_status',)
        
class AddressForm(ModelForm):
    class Meta:
        fields = '__all__'
        textWidget = TextInput(attrs={'class':'long-input'})
        model = Address
        widgets = {
                    'address':textWidget,
                  } 


class DevProfileForm(ModelForm):
    client_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    def __init__(self, *args, **kwargs):
        super(DevProfileForm, self).__init__(*args, **kwargs)
        multi_fields = ('coverage_regions', 'coverage_localities', 'gears',)
        for multi_field in multi_fields:
            self.fields[multi_field].help_text = ''        
    class Meta:
        fields = ['coverage_regions', 'coverage_localities', 'quality', 'experience', 'transport', 'gears', 'bad_habits', 'progress', 'pc_skills', 'note',]
        model = DevProfile
        widgets = {
                    'coverage_regions':AutoComboboxSelectMultipleWidget(RegionLookup), 
                    'coverage_localities':AutoCompleteSelectMultipleWidget(LocalityLookup),                  
                    'quality':AutoComboboxSelectWidget(QualityLookup),                                      
                    'experience':AutoComboboxSelectWidget(ExperienceLookup),
                    'note': Textarea(attrs={'rows':'5'}),
                  }


class ExtraProfileForm(ModelForm):
    client_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    def __init__(self, *args, **kwargs):
        super(ExtraProfileForm, self).__init__(*args, **kwargs)        
    class Meta:
        fields = ['last_name','first_name','patronymic','gender','citizenship','birthday','birthplace','passport_series','passport_number']
        exclude = ['address',]
        model = ExtraProfile
        widgets = {
                    'citizenship':AutoComboboxSelectWidget(CitizenshipLookup),
                    'birthday': DateTimeInput(attrs={'class':'date-input'}, format='%d.%m.%Y'),
                    'gender': forms.RadioSelect,
                  }


class RequiredWorkTypeProfileFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return                
        for data in self.cleaned_data:            
            if 'DELETE' in data and not data['DELETE']:
                return  
        raise ValidationError(u'В профиле нужно указать хотябы один вид работ!')


class WorkTypeProfileFormInlineForm(ModelForm):
    price_min = LocalIntegerField(label=_('Price min'))
    price_max = LocalIntegerField(label=_('Price max'))
    class Meta:
        fields = '__all__'
        model = WorkTypeProfile
        widgets = {                   
                    'quality':AutoComboboxSelectWidget(QualityLookup),                                      
                    'experience':AutoComboboxSelectWidget(ExperienceLookup),   
                    'work_type':AutoComboboxSelectWidget(WorkTypeLookup),
                    'measure':AutoComboboxSelectWidget(MeasureLookup, attrs={'class':'short-input'}),                                   
                    'note':TextInput(),
                  }
        

WorkTypeProfileFormSet = inlineformset_factory(DevProfile, WorkTypeProfile, extra=1, form=WorkTypeProfileFormInlineForm)


class GoodsProfileM2MInlineForm(ModelForm):
    price = LocalIntegerField(label=_('Price min'))    
    class Meta:
        fields = '__all__'
        model = GoodsProfileM2M
        widgets = {
                   'goods':AutoComboboxSelectWidget(GoodsLookup), 
                   'measure':AutoComboboxSelectWidget(MeasureLookup),
                   }
        

GoodsProfileM2MFormSet = inlineformset_factory(DevProfile, GoodsProfileM2M, extra=1, form=GoodsProfileM2MInlineForm)


class PartnerFilterForm(Form):
    pk = AutoCompleteSelectMultipleField(
            lookup_class=PartnerIdLookup,
            label=_('ID'),
            required=False            
        )
    created = DateRangeField(required=False, label=_('Created'))
    created_by = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=ExUserLookup, label=u'Кем создано', required=False)       
    updated = DateRangeField(required=False, label=_('Updated'))
    updated_by = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=ExUserLookup, label=u'Кем обновлено', required=False)
    partner_types = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=PartnerTypeLookup,
            label=_('Partner type'),
            required=False,
        )
    name = forms.CharField(required=False, label=_('Name'))
    address = forms.CharField(required=False, label=_('Address'))
    note = forms.CharField(required=False, label=_('Note'))
#     next = forms.CharField(required=False, widget=forms.HiddenInput())    
    def get_filter(self):
        if self.is_valid():
            return self.make_filter(self.cleaned_data)
        return {}
            
    def make_filter(self, cleaned_data):
        f = {}
        if not cleaned_data:
            return f        
        
        q = Q()
        address = cleaned_data['address']
        if address:
            parts = address.split()
            for part in parts:
                q = q | Q(address__address__icontains=part) | Q(address__region__icontains=part) | Q(address__locality__icontains=part)
        
        if len(q):
            f['Q'] = q 
        
        history_fields = ('created','updated')
        for fld in history_fields:
            cleaned_value = cleaned_data[fld]
            if cleaned_value:
                value = history_filter(cleaned_value, fld)
                if value:                 
                    f.update(value)
        
        if cleaned_data['pk']:
            f['id__in'] = [item.pk for item in cleaned_data['pk']]
        
        simple_filter = { 
                          'history__created_by__in': 'created_by',
                          'history__updated_by__in': 'updated_by',
                          'partner_type__in': 'partner_types',
                          'name__icontains': 'name',
                          'address__icontains': 'client_type',                                                   
                          'note__icontains': 'note',
                         }
        
        for key, value in simple_filter.iteritems():
            if value in cleaned_data and cleaned_data[value]:                
                f[key] = cleaned_data[value]
                        
        return f  
        