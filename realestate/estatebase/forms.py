# -*- coding: utf-8 -*-

from estatebase.lookups import StreetLookup, LocalityLookup, MicrodistrictLookup,\
    EstateTypeLookup, EstateLookup
from django.forms import ModelForm
from estatebase.models import  Client, Contact, ClientType, \
    Origin, ContactHistory, Bidg, Estate, Document, Layout, Level, EstatePhoto, get_polymorph_label, \
    Stead, EstateType, Region, Street
from django import forms

from selectable.forms import AutoCompleteSelectWidget
from django.forms.widgets import Textarea, TextInput, DateTimeInput
from django.forms.models import inlineformset_factory
from django.forms.forms import Form
from django.utils.translation import ugettext_lazy as _
from selectable.forms.widgets import AutoComboboxSelectWidget
from django.forms.formsets import formset_factory, BaseFormSet
from selectable.forms.fields import AutoCompleteSelectField,\
    AutoCompleteSelectMultipleField



class EstateCreateForm(ModelForm):
    #estate_type = forms.ModelChoiceField(queryset=EstateType.objects.all(), widget=forms.HiddenInput())         
    class Meta:                
        model = Estate
        fields = ('estate_type', 'origin', 'region', 'locality', 'microdistrict', 'street', 'estate_number',
                  'beside', 'beside_distance', 'saler_price', 'agency_price', 'estate_status', 'estate_type')
        widgets = {
            'street': AutoCompleteSelectWidget(StreetLookup),
            'locality': AutoComboboxSelectWidget(LocalityLookup),
            'microdistrict' : AutoComboboxSelectWidget(MicrodistrictLookup),
        }

class EstateCommunicationForm(ModelForm):
    class Meta:                
        model = Estate
        fields = ('electricity', 'electricity_distance', 'watersupply', 'watersupply_distance',
                  'gassupply', 'gassupply_distance', 'sewerage', 'sewerage_distance', 'telephony',
                  'internet', 'driveway', 'driveway_distance',)


class EstateParamForm(ModelForm):
    class Meta:                
        model = Estate
        fields = ('estate_params', 'description', 'comment')
        widgets = {
           'estate_params' : forms.CheckboxSelectMultiple()        
        }
    

class ClientForm(ModelForm):              
    class Meta:        
        exclude = ('created_by', 'updated', 'created', 'updated_by')
        model = Client
        widgets = {
            'note': Textarea(attrs={'rows':'5'}),
            'address' : TextInput(attrs={'class': 'big-text-input'}),
            'created' : DateTimeInput(attrs={'readonly':'True'}, format='%d.%m.%Y %H:%M'),
        }

class ClientFilterForm(Form):
    pk = forms.IntegerField(required=False, label=_('ID'))
    contact = forms.CharField(required=False, label=_('Contact'))
    name = forms.CharField(required=False, label=_('Name'))
    client_type = forms.ModelChoiceField(ClientType.objects.all(), required=False, label=_('ClientType'))
    origin = forms.ModelChoiceField(Origin.objects.all(), required=False, label=_('Origin'))
    address = forms.CharField(required=False, label=_('Address'))
    note = forms.CharField(required=False, label=_('Note'))
    next = forms.CharField(required=False, widget=forms.HiddenInput())
    filters = {
            'pk' : 'id__exact',
            'contact' : 'contacts__contact__icontains',
            'client_type' : 'client_type__id__exact',
            'name' : 'name__icontains',
            'origin' : 'origin__id__exact',
            'address' : 'address__icontains',
            'note' : 'note__icontains',
    }    
    def get_filter(self):
        f = {}   
        for field in self.fields:
            value = self[field].value()
            if value and self.filters.has_key(field):                
                f[self.filters[field]] = value      
        return f            

class EstateFilterForm(Form):
    pk = AutoCompleteSelectMultipleField(
            lookup_class=EstateLookup,
            label=_('ID'),
            required=False,
        ) 
    estate_type = AutoCompleteSelectMultipleField(
            lookup_class=EstateTypeLookup,
            label=_('Estate type'),
            required=False,
        ) 
    street = AutoCompleteSelectMultipleField(
            lookup_class=StreetLookup,
            label=_('Street'),
            required=False,
        )   
    def get_filter(self):
        f = {}   
        if self['pk'].value():                                 
            f['id__in'] = self['pk'].value()
        if self['street'].value():
            f['street_id__in'] = self['street'].value()
        if self['estate_type'].value():
            f['estate_type_id__in'] = self['estate_type'].value()                
        return f     
        
class ContactHistoryForm(ModelForm):
    class Meta:        
        model = ContactHistory
        widgets = {
            'event_date': DateTimeInput(attrs={'readonly':'True'}, format='%d.%m.%Y %H:%M'),
        }            
        
class ContactInlineForm(ModelForm):
    class Meta:
        model = Contact        
        
ContactFormSet = inlineformset_factory(Client, Contact, extra=1, form=ContactInlineForm)
ContactHistoryFormSet = inlineformset_factory(Contact, ContactHistory, extra=1, form=ContactHistoryForm)

class ContactForm(ModelForm):     
    class Meta:        
        fields = ('contact', 'contact_state')
        model = Contact    


class BidgForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BidgForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['documents'].queryset = Document.objects.filter(estate_type__id=self.instance.estate_type_id)
        self.fields['documents'].help_text = ''
    estate = forms.ModelChoiceField(queryset=Estate.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = Bidg
        widgets = {
           'documents' : forms.CheckboxSelectMultiple()        
        }

class ApartmentForm(BidgForm):    
    def __init__(self, *args, **kwargs):
        super(ApartmentForm, self).__init__(*args, **kwargs)
        field_to_delete = []
        fields = self.instance.all_fields[:] 
        extra = ['documents']
        if not self.instance.basic:
            extra.append('estate_type')
        fields.extend(extra)        
        for field in self.fields:            
            if field not in fields:
                field_to_delete.append(field)                
            else:                                
                self.fields[field].label = get_polymorph_label(self.instance, field)                           
        for field in field_to_delete:
            del self.fields[field]                                                  
    class Meta(BidgForm.Meta):
        pass        
        
class LayoutForm(ModelForm):
    class Meta:
        model = Layout        

LevelFormSet = inlineformset_factory(Level, Layout, extra=1, form=LayoutForm)

class LevelForm(ModelForm):
    bidg = forms.ModelChoiceField(queryset=Bidg.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = Level

class ImageUpdateForm(ModelForm):
    class Meta:
        model = EstatePhoto   
        fields = ('name', 'note', 'image')     

class SteadUpdateForm(ModelForm):
    class Meta:
        model = Stead   
        exclude = ('estate',)
                    
