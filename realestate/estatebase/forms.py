# -*- coding: utf-8 -*-

from estatebase.lookups import StreetLookup
from django.forms import ModelForm
from estatebase.models import Estate, EstateType
from django import forms

from selectable.forms import AutoCompleteSelectWidget

class EstateForm(ModelForm):
    estate_type=forms.ModelChoiceField(queryset=EstateType.objects.all(),widget=forms.HiddenInput())         
    class Meta:
        model = Estate
        widgets = {
            'street': AutoCompleteSelectWidget(StreetLookup)
        }

    