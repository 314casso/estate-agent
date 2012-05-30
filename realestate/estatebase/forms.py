# -*- coding: utf-8 -*-

from estatebase.lookups import StreetLookup
from django.forms import ModelForm
from estatebase.models import Estate, EstateType, Client, Contact, ClientType, \
    Origin, ContactHistory
from django import forms

from selectable.forms import AutoCompleteSelectWidget
from django.forms.widgets import Textarea, TextInput, DateTimeInput
from django.forms.models import inlineformset_factory
from django.forms.forms import Form
from django.utils.translation import ugettext_lazy as _

class EstateForm(ModelForm):
    estate_type = forms.ModelChoiceField(queryset=EstateType.objects.all(), widget=forms.HiddenInput())         
    class Meta:
        model = Estate
        widgets = {
            'street': AutoCompleteSelectWidget(StreetLookup)
        }

class ClientForm(ModelForm):              
    class Meta:        
        exclude = ('created_by','updated','created', 'updated_by')
        model = Client
        widgets = {
            'note': Textarea(attrs={'rows':'5'}),
            'address' : TextInput(attrs={'class': 'big-text-input'}),
            'created' : DateTimeInput(attrs={'readonly':'True'},format = '%d.%m.%Y %H:%M'),                        
        }

class ClientFilterForm(Form):
    pk = forms.IntegerField(required=False, label=_('ID'))
    contact = forms.CharField(required=False, label=_('Contact'))
    name = forms.CharField(required=False, label=_('Name'))
    client_type = forms.ModelChoiceField(ClientType.objects.all(), required=False, label=_('ClientType'))
    origin = forms.ModelChoiceField(Origin.objects.all(), required=False, label=_('Origin'))
    address = forms.CharField(required=False, label=_('Address'))
    note = forms.CharField(required=False, label=_('Note'))
    filters = {
            'pk' : 'id__exact',   
            'contact' : 'contactlist__contact__icontains',   
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
        
class ContactHistoryForm(ModelForm):
    class Meta:        
        model = ContactHistory
        widgets = {
            'event_date': DateTimeInput(attrs={'readonly':'True'},format = '%d.%m.%Y %H:%M'),            
        }            
        
class ContactInlineForm(ModelForm):
    class Meta:
        model = Contact        
        
ContactFormSet = inlineformset_factory(Client, Contact, extra=1, form=ContactInlineForm)
ContactHistoryFormSet = inlineformset_factory(Contact, ContactHistory, extra=1, form=ContactHistoryForm)

class ContactForm(ModelForm):
    class Meta:        
        model = Contact
        widgets = {
            'event_date': DateTimeInput(attrs={'readonly':'True'},format = '%d.%m.%Y %H:%M'),            
        }   
    
