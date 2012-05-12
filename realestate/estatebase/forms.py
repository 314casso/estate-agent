# -*- coding: utf-8 -*-

from estatebase.lookups import StreetLookup
from django.forms import ModelForm
from estatebase.models import Estate, EstateType, Client
from django import forms

from selectable.forms import AutoCompleteSelectWidget
from django.forms.widgets import Textarea



class EstateForm(ModelForm):
    estate_type=forms.ModelChoiceField(queryset=EstateType.objects.all(),widget=forms.HiddenInput())         
    class Meta:
        model = Estate
        widgets = {
            'street': AutoCompleteSelectWidget(StreetLookup)
        }

class ClientForm(ModelForm):             
    class Meta:
        model = Client
        widgets = {
            'note': Textarea()
        }            