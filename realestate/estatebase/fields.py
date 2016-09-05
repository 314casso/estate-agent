# -*- coding: utf-8 -*-
from django import forms
from selectable.forms.widgets import AutoComboboxSelectWidget
from django.forms.widgets import TextInput, DateInput
from django.forms.fields import MultiValueField, CharField, IntegerField, \
    DateField, DecimalField
from selectable.forms.fields import  AutoCompleteSelectField
from django.utils.translation import ugettext_lazy as _

class ComplexFieldWidget(forms.MultiWidget):
    def __init__(self, lookup_class, attrs=None):                
        widgets = (AutoComboboxSelectWidget(lookup_class), TextInput(attrs={'class':'number-input'}))
        super(ComplexFieldWidget, self).__init__(widgets, attrs)
    def decompress(self, value):
        if value:            
            return value
        return [None, None] 

class ComplexField(MultiValueField):
    help_text = u'Испозьуйте > < и дефис для указания диапазона в числовом поле'
    def __init__(self, lookup_class, *args, **kwargs):
        self.widget = ComplexFieldWidget(lookup_class=lookup_class, attrs={'title':self.help_text})        
        fields = []
#TODO:         Use AutoCompleteSelectField with a AutoComboboxSelectWidget instead.
        fields.append(AutoCompleteSelectField(
            lookup_class=lookup_class,
            required=False,
            #widget=AutoComboboxSelectWidget
            )
         )        
        fields.append(CharField())        
        super(ComplexField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:                        
            return data_list
        return [None, None]

class LocalIntegerField(IntegerField):
    widget = TextInput(attrs={'class':'local-int'})
    def __init__(self, max_value=None, min_value=None, required=False, *args, **kwargs):
        super(LocalIntegerField, self).__init__(max_value, min_value, required, localize=True, *args, **kwargs)

class LocalDecimalField(DecimalField):
    widget = TextInput(attrs={'class':'local-decimal'})
    def __init__(self, max_value=None, min_value=None, max_digits=None, decimal_places=2, required=False, *args, **kwargs):
        super(LocalDecimalField, self).__init__(max_value, min_value,max_digits, decimal_places, required, localize=True, *args, **kwargs)

class DateRangeWidget(forms.MultiWidget):
    def __init__(self, attrs=None, date_format=None):
        date_input = DateInput(attrs={'class':'date-input', 'pattern':'(((0[1-9]|[12]\d|3[01])\.(0[13578]|1[02])\.((19|[2-9]\d)\d{2}))|((0[1-9]|[12]\d|30)\.(0[13456789]|1[012])\.((19|[2-9]\d)\d{2}))|((0[1-9]|1\d|2[0-8])\.02\.((19|[2-9]\d)\d{2}))|(29\.02\.((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00))))'}, format=date_format)
        widgets = (date_input, date_input)
        super(DateRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:            
            return value
        return [None, None]    

class DateRangeField(MultiValueField):
    widget = DateRangeWidget    
    default_error_messages = {
        'invalid_date': _(u'Enter a valid date.'),
    }
    def __init__(self, input_date_formats=None, input_time_formats=None, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)
        field = DateField(input_formats=input_date_formats,
                      error_messages={'invalid': errors['invalid_date']},
                      localize=localize)
        fields = (field, field,)
        super(DateRangeField, self).__init__(fields, *args, **kwargs)
    def compress(self, data_list):
        if data_list:                        
            return data_list
        return [None, None]
    
class NumberRangeWidget(forms.MultiWidget):
    is_localized = True
    def __init__(self, attrs=None):
        text_input = TextInput(attrs=attrs)
        widgets = (text_input, text_input)
        super(NumberRangeWidget, self).__init__(widgets, attrs)
    def decompress(self, value):
        if value:            
            return value
        return [None, None]    

class DecimalRangeField(MultiValueField):       
    def __init__(self, max_value=None, min_value=None, max_digits=None, decimal_places=None, *args, **kwargs):
        self.widget = NumberRangeWidget(attrs={'class':'local-decimal'})
        errors = DecimalField.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', True)
        field = DecimalField(max_value, min_value, max_digits, decimal_places, localize=localize)
        fields = (field, field,)
        super(DecimalRangeField, self).__init__(fields, *args, **kwargs)
    def compress(self, data_list):
        if data_list:                        
            return data_list
        return [None, None]
    
class IntegerRangeField(MultiValueField):       
    def __init__(self, max_value=None, min_value=None, *args, **kwargs):
        self.widget = NumberRangeWidget(attrs={'class':'local-int'})
        errors = IntegerField.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', True)        
        field = IntegerField(max_value, min_value, localize=localize)
        fields = (field, field,)
        super(IntegerRangeField, self).__init__(fields, *args, **kwargs)
    def compress(self, data_list):
        if data_list:                        
            return data_list
        return [None, None]   
