# -*- coding: utf-8 -*-

from estatebase.lookups import StreetLookup, LocalityLookup, MicrodistrictLookup,\
    EstateTypeLookup, EstateLookup, RegionLookup, EstateStatusLookup,\
    WallConstrucionLookup
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
    AutoCompleteSelectMultipleField, AutoComboboxSelectMultipleField
import re



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
    region = AutoComboboxSelectMultipleField(
            lookup_class=RegionLookup,
            label=_('Region'),
            required=False,
        )    
    locality = AutoComboboxSelectMultipleField(
            lookup_class=LocalityLookup,
            label=_('Locality'),
            required=False,
        )    
    microdistrict = AutoCompleteSelectMultipleField(
            lookup_class=MicrodistrictLookup,
            label=_('Microdistrict'),
            required=False,
        )     
    street = AutoCompleteSelectMultipleField(
            lookup_class=StreetLookup,
            label=_('Street'),
            required=False,
        )    
    estate_number = forms.CharField(required=False, label=_('Estate number'))
    room_number = forms.CharField(required=False, label=_('Room number'))    
    estate_status = AutoComboboxSelectMultipleField(
            lookup_class=EstateStatusLookup,
            label=_('Estate status'),
            required=False,
        )         
    agency_price = forms.CharField(required=False, label=_('Price'))    
    client = forms.CharField(required=False, label=_('Client'))
    contact = forms.CharField(required=False, label=_('Contact'))
    year_built = forms.CharField(required=False, label=_('Year built'))
    floor = forms.CharField(required=False, label=_('Floor'))        
    floor_count = forms.CharField(required=False, label=_('Floor count'))
    wall_construcion = AutoComboboxSelectMultipleField(
            lookup_class=WallConstrucionLookup,
            label=_('Wall Construcion'),
            required=False,
        )
    total_area = forms.CharField(required=False, label=_('Total area'))
    used_area = forms.CharField(required=False, label=_('Used area'))   
    room_count = forms.CharField(required=False, label=_('Room count'))
    stead_area = forms.CharField(required=False, label=_('Stead area'))
    def get_filter(self):
        f = {}   
        if self['pk'].value():                                 
            f['id__in'] = self['pk'].value()
        if self['street'].value():
            f['street_id__in'] = self['street'].value()
        if self['estate_type'].value():
            f['estate_type_id__in'] = self['estate_type'].value()                
        if self['region'].value():
            f['region_id__in'] = self['region'].value()
        if self['locality'].value():
            f['locality_id__in'] = self['locality'].value()
        if self['estate_number'].value():                                 
            f['estate_number__in'] = split_string(self['estate_number'].value())
        if self['room_number'].value():                                 
            f['bidgs__room_number__contains'] = self['room_number'].value()
        if self['microdistrict'].value():
            f['microdistrict_id__in'] = self['microdistrict'].value()
        if self['estate_status'].value():
            f['estate_status_id__in'] = self['estate_status'].value()                                           
        if self['client'].value():
            f['clients__name__icontains'] = self['client'].value()    
        if self['contact'].value():
            f['clients__contacts__contact__icontains'] = self['contact'].value()    
        if self['agency_price'].value():
            value = from_to(self['agency_price'].value(),'agency_price')
            if value:
                f.update(value)    
        if self['year_built'].value():
            value = from_to(self['year_built'].value(),'bidgs__year_built')
            if value:
                f.update(value)
        if self['floor'].value():
            value = from_to(self['floor'].value(),'bidgs__floor')
            if value:
                f.update(value)        
        if self['floor_count'].value():
            value = from_to(self['floor_count'].value(),'bidgs__floor_count')
            if value:
                f.update(value)                
        if self['wall_construcion'].value():
            f['bidgs__wall_construcion_id__in'] = self['wall_construcion'].value()            
        if self['total_area'].value():
            value = from_to(self['total_area'].value(),'bidgs__total_area')
            if value:
                f.update(value)            
        if self['used_area'].value():
            value = from_to(self['used_area'].value(),'bidgs__used_area')
            if value:
                f.update(value)        
        if self['room_count'].value():
            value = from_to(self['room_count'].value(),'bidgs__room_count')
            if value:
                f.update(value)        
        if self['stead_area'].value():
            value = from_to(self['stead_area'].value(),'stead__total_area')
            if value:
                f.update(value)        
        return f     

'''
Для формирование поля от до
'''
def from_to(value,field_name):
    f = {}
    if not value:
        return None    
    a = ''.join(value.split())
    matchobjs = re.match(r"^(?P<oper>\>|\<)(?P<n>\d+)$", a)
    if matchobjs:         
        if matchobjs.group('oper') == '>':
            f['%s__gte' % field_name] = matchobjs.group('n')
        else:
            f['%s__lte' % field_name] = matchobjs.group('n')    
    else:
        matchobjs = re.match(r"^(?P<n1>\d+)\-(?P<n2>\d+)$", a)
        if matchobjs:
            f['%s__range' % field_name] = (matchobjs.group('n1'), matchobjs.group('n2'))            
        else:
            matchobjs = re.match(r"^(?P<n>\d+)$", a)
            if matchobjs:
                f['%s__exact' % field_name] = matchobjs.group('n')   
    return f or None    

def split_string(value):                 
    return [int(x.strip()) for x in value.split(',')]     
        
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
                    
