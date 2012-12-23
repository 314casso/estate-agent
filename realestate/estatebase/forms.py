# -*- coding: utf-8 -*-
from django import forms
from django.db.models.query_utils import Q
from django.forms import ModelForm
from django.forms.forms import Form
from django.forms.models import inlineformset_factory, \
    BaseInlineFormSet
from django.forms.widgets import Textarea, TextInput, DateTimeInput, \
    CheckboxInput
from django.utils.translation import ugettext_lazy as _
from estatebase.field_utils import from_to_values, split_string, \
    complex_field_parser, check_value_list
from estatebase.fields import ComplexField, LocalIntegerField, DateRangeField, \
    IntegerRangeField, DecimalRangeField, LocalDecimalField
from estatebase.lookups import StreetLookup, LocalityLookup, MicrodistrictLookup, \
    EstateTypeLookup, EstateLookup, RegionLookup, EstateStatusLookup, \
    WallConstrucionLookup, OriginLookup, BesideLookup, InteriorLookup, \
    ElectricityLookup, WatersupplyLookup, GassupplyLookup, SewerageLookup, \
    DrivewayLookup, ClientLookup, ContactLookup, ExUserLookup, ClientIdLookup, \
    ClientTypeLookup, BidIdLookup, EstateRegisterIdLookup, EstateTypeCategoryLookup, \
    ComChoiceLookup, InternetLookup, TelephonyLookup, LayoutTypeLookup, \
    LevelNameLookup, EstateClientStatusLookup, ShapeLookup, EstateParamLookup,\
    ValidityLookup, ApplianceLookup, BidEventCategoryLookup,\
    RegisterCategoryLookup, ExteriorFinishLookup, BidStatusLookup
from estatebase.models import Client, Contact, ContactHistory, Bidg, Estate, \
    Document, Layout, Level, EstatePhoto, Stead, Bid, EstateRegister, \
    EstateType, EstateClient, BidEvent
from estatebase.wrapper import get_polymorph_label, get_wrapper
from form_utils.forms import BetterForm, BetterModelForm
from selectable.forms import AutoCompleteSelectWidget
from selectable.forms.fields import AutoCompleteSelectMultipleField, \
    AutoComboboxSelectMultipleField, AutoComboboxSelectField, \
    AutoCompleteSelectField
from selectable.forms.widgets import AutoComboboxSelectWidget,\
    AutoComboboxSelectMultipleWidget
from settings import CORRECT_DELTA
from django.utils.safestring import mark_safe
from django.template.base import Template
from django.core.exceptions import ValidationError

class EstateForm(BetterModelForm):              
    beside_distance = LocalIntegerField(label='')
    agency_price = LocalIntegerField(label=_('Agency price'))
    saler_price = LocalIntegerField(label=_('Saler price'))
    class Meta:                
        model = Estate
        fields = ('origin', 'region', 'locality', 'microdistrict', 'street', 'estate_number',
                  'beside', 'beside_distance', 'saler_price', 'agency_price', 'estate_status', 'broker', 'com_status')
        widgets = {
            'estate_status': AutoComboboxSelectWidget(EstateStatusLookup),
            'beside':AutoComboboxSelectWidget(BesideLookup),
            'region': AutoComboboxSelectWidget(RegionLookup),
            'origin': AutoComboboxSelectWidget(OriginLookup),
            'street': AutoCompleteSelectWidget(StreetLookup),
            'locality': AutoComboboxSelectWidget(LocalityLookup),
            'microdistrict' : AutoComboboxSelectWidget(MicrodistrictLookup),
            'broker': AutoComboboxSelectWidget(ExUserLookup),
            'com_status': AutoComboboxSelectWidget(ComChoiceLookup),
        }

class EstateCreateForm(EstateForm):
    estate_category_filter = AutoComboboxSelectField(
            lookup_class=EstateTypeCategoryLookup,
            label=_('EstateTypeCategory'),
            required=False
        )
    estate_type = AutoComboboxSelectField(
            lookup_class=EstateTypeLookup,
            label=_('Estate type')
        )
    class Meta(EstateForm.Meta):        
        fields = ('estate_category_filter', 'estate_type', 'origin', 'region', 'locality', 'microdistrict', 'street', 'estate_number',
                  'beside', 'beside_distance', 'saler_price', 'agency_price', 'estate_status', 'estate_type', 'broker', 'com_status')

class EstateCreateClientForm(EstateCreateForm):
    client_status = AutoComboboxSelectField(lookup_class=EstateClientStatusLookup, label=_('Estate client status'))
    client = AutoCompleteSelectField(
            lookup_class=ClientLookup,
            label=_('Client'),
            required=True,
        )
    def __init__(self, *args, **kwargs):
        super(EstateCreateClientForm, self).__init__(*args, **kwargs)
        self.fields['client'].widget.attrs = {'class':'long-input'}
        
class EstateCreateWizardForm(EstateCreateClientForm):
    class Meta(EstateCreateClientForm.Meta):        
        fields = ('client', 'client_status', 'estate_category_filter', 'estate_type', 'origin', 'region', 'locality', 'microdistrict', 'street', 'estate_number',
                  'beside', 'beside_distance', 'saler_price', 'agency_price', 'estate_status', 'estate_type', 'broker', 'com_status')

class EstateCommunicationForm(ModelForm):
    class Meta:                
        model = Estate
        fields = ('electricity', 'electricity_distance', 'watersupply', 'watersupply_distance',
                  'gassupply', 'gassupply_distance', 'sewerage', 'sewerage_distance', 'telephony',
                  'internet', 'driveway', 'driveway_distance',)
        widgets = {
                   'electricity':AutoComboboxSelectWidget(ElectricityLookup),
                   'gassupply':AutoComboboxSelectWidget(GassupplyLookup),
                   'watersupply':AutoComboboxSelectWidget(WatersupplyLookup),
                   'sewerage':AutoComboboxSelectWidget(SewerageLookup),
                   'internet':AutoComboboxSelectWidget(InternetLookup),
                   'telephony':AutoComboboxSelectWidget(TelephonyLookup),
                   'driveway':AutoComboboxSelectWidget(DrivewayLookup),
                  }

class EstateParamForm(ModelForm):
    class Meta:                
        model = Estate
        fields = ('estate_params', 'description', 'comment')
        widgets = {
           'estate_params' : forms.CheckboxSelectMultiple()        
        }

class ClientForm(ModelForm):   
    origin = AutoComboboxSelectField(
            lookup_class=OriginLookup,
            label=_('Origin'),
            required=False,
        )               
    class Meta:        
#        exclude = ('created_by', 'updated', 'created', 'updated_by', 'deleted')
        fields = ['origin','client_type', 'name', 'address', 'note']
        model = Client
        widgets = {
            'note': Textarea(attrs={'rows':'5'}),
            'address' : TextInput(attrs={'class': 'big-text-input'}),
            'created' : DateTimeInput(attrs={'readonly':'True'}, format='%d.%m.%Y %H:%M'),
            'valid' : CheckboxInput(attrs={'disabled':'disabled'}),
        }

class ClientFilterForm(Form):
    pk = AutoCompleteSelectMultipleField(
            lookup_class=ClientIdLookup,
            label=_('ID'),
            required=False            
        )
    created = DateRangeField(required=False, label=_('Created'))        
    updated = DateRangeField(required=False, label=_('Updated'))
    origin = AutoComboboxSelectMultipleField(
            lookup_class=OriginLookup,
            label=_('Origin'),
            required=False,
        )
    client_type = AutoComboboxSelectMultipleField(
            lookup_class=ClientTypeLookup,
            label=_('ClientType'),
            required=False,
        )
    name = forms.CharField(required=False, label=_('Name'))
    address = forms.CharField(required=False, label=_('Address'))
    contacts = AutoCompleteSelectMultipleField(
            lookup_class=ContactLookup,
            label=_('Contact'),
            required=False,
        )
    note = forms.CharField(required=False, label=_('Note'))
    next = forms.CharField(required=False, widget=forms.HiddenInput())        
    def get_filter(self):
        f = {}
        if self['pk'].value():
            f['id__in'] = self['pk'].value()
        if self['created'].value():            
            value = from_to_values(self['created'].field.clean(self['created'].value()), 'history__created')            
            if value:                 
                f.update(value)        
        if self['updated'].value():            
            value = from_to_values(self['updated'].field.clean(self['updated'].value()), 'history__updated')            
            if value:                 
                f.update(value)
        if self['contacts'].value():
            f['contacts__id__in'] = self['contacts'].value()
        if self['name'].value():
            f['name__icontains'] = self['name'].value()
        if self['client_type'].value():
            f['client_type_id__in'] = self['client_type'].value()
        if self['origin'].value():
            f['origin_id__in'] = self['origin'].value()                                                    
        if self['address'].value():
            f['address__icontains'] = self['address'].value()    
        if self['note'].value():
            f['note__icontains'] = self['note'].value()    
        return f   
               
class EstateFilterForm(BetterForm):
    validity = AutoComboboxSelectMultipleField(
            lookup_class=ValidityLookup,
            label=_('Validity'),
            required=False,
        )
    estates = AutoCompleteSelectMultipleField(
            lookup_class=EstateLookup,
            label=_('ID'),
            required=False,
        )
    estate_category = AutoComboboxSelectMultipleField(
            lookup_class=EstateTypeCategoryLookup,
            label=_('EstateTypeCategory'),
            required=False,
        )
    estate_type = AutoCompleteSelectMultipleField(
            lookup_class=EstateTypeLookup,
            label=_('Estate type'),
            required=False,
        )
    com_status = AutoComboboxSelectMultipleField(
            lookup_class=ComChoiceLookup,
            label=_('Commerce'),
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
    agency_price = IntegerRangeField(label=_('Price'), required=False)    
    clients = AutoCompleteSelectMultipleField(
            lookup_class=ClientLookup,
            label=_('Client'),
            required=False,
        )
    contacts = AutoCompleteSelectMultipleField(
            lookup_class=ContactLookup,
            label=_('Contact'),
            required=False,
        )    
    year_built = IntegerRangeField(required=False, label=_('Year built'))
    floor = IntegerRangeField(required=False, label=_('Floor'))        
    floor_count = IntegerRangeField(required=False, label=_('Floor count'))
    wall_construcion = AutoComboboxSelectMultipleField(
            lookup_class=WallConstrucionLookup,
            label=_('Wall Construcion'),
            required=False,
        )
    total_area = DecimalRangeField(required=False, label=_('Total area'))
    used_area = DecimalRangeField(required=False, label=_('Used area'))   
    room_count = IntegerRangeField(required=False, label=_('Room count'))
    stead_area = DecimalRangeField(required=False, label=_('Stead area'))
    
    created = DateRangeField(required=False, label=_('Created'))        
    updated = DateRangeField(required=False, label=_('Updated'))
    origin = AutoComboboxSelectMultipleField(
            lookup_class=OriginLookup,
            label=_('Origin'),
            required=False,
        )  
    beside = ComplexField(required=False, label=_('Beside'), lookup_class=BesideLookup)
    interior = AutoComboboxSelectMultipleField(
            lookup_class=InteriorLookup,
            label=_('Interior'),
            required=False,
        )
    exterior_finish = AutoComboboxSelectMultipleField(
            lookup_class=ExteriorFinishLookup,
            label=_('Exterior finish'),
            required=False,
        )    
    face_area = DecimalRangeField(required=False, label=_('Face area'))
    shape = AutoComboboxSelectMultipleField(
            lookup_class=ShapeLookup,
            label=_('Shape'),
            required=False,
        ) 
    electricity = ComplexField(required=False, label=_('Electricity'), lookup_class=ElectricityLookup)
    watersupply = ComplexField(required=False, label=_('Watersupply'), lookup_class=WatersupplyLookup)    
    gassupply = ComplexField(required=False, label=_('Gassupply'), lookup_class=GassupplyLookup)    
    sewerage = ComplexField(required=False, label=_('Sewerage'), lookup_class=SewerageLookup)
    driveway = ComplexField(required=False, label=_('Driveway'), lookup_class=DrivewayLookup)
    
    marks = AutoComboboxSelectMultipleField(
            lookup_class=EstateParamLookup,
            label=_('Estate params'),
            required=False,
        ) 
    
    FOTO_CHOICES = ((3, u'Все',), (0, u'Нет фото',), (1, u'Есть фото',))
    foto_choice = forms.ChoiceField(label=_('EstatePhoto'), widget=forms.RadioSelect, choices=FOTO_CHOICES, initial=3, required=False,)
    description = forms.CharField(required=False, label=_('Description'))
    comment = forms.CharField(required=False, label=_('Comment'))
    next = forms.CharField(required=False, widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        super(EstateFilterForm, self).__init__(*args, **kwargs)
        self.fields['next'].label = ''
    def type_filter(self):
        q = Q()
        cats = self['estate_category'].field.clean(self['estate_category'].value())         
        types = self['estate_type'].field.clean(self['estate_type'].value())        
        for t in types:
            if t.estate_type_category in cats:
                cats.remove(t.estate_type_category)
            q = Q(bidgs__estate_type_id__exact=t.pk, estate_category_id__exact=t.estate_type_category_id)
            q = q | Q(stead__estate_type_id__exact=t.pk, estate_category_id__exact=t.estate_type_category_id)
        if len(cats):
            q = q | Q(estate_category__in=cats)
        return q
        
    def get_filter(self):
        f = {}
        q = self.type_filter()        
        if len(q):
            f['Q'] = q       
        if self['com_status'].value():
            f['com_status_id__in'] = self['com_status'].value()
        if self['validity'].value():
            f['validity_id__in'] = self['validity'].value()
            f['history__modificated__gt'] = CORRECT_DELTA
        if self['estates'].value():                                 
            f['id__in'] = self['estates'].value()        
        if self['region'].value():
            f['region_id__in'] = self['region'].value()
        if self['locality'].value():
            f['locality_id__in'] = self['locality'].value()            
        if self['microdistrict'].value():
            f['microdistrict_id__in'] = self['microdistrict'].value()    
        if self['street'].value():
            f['street_id__in'] = self['street'].value()                    
        if self['estate_number'].value():                                 
            f['estate_number__in'] = split_string(self['estate_number'].value())
        if self['room_number'].value():                                 
            f['bidgs__room_number__contains'] = self['room_number'].value()        
        if self['estate_status'].value():
            f['estate_status_id__in'] = self['estate_status'].value()                                           
        if self['clients'].value():
            f['clients__id__in'] = self['clients'].value()    
        if self['contacts'].value():
            f['clients__contacts__id__in'] = self['contacts'].value()
        if self['shape'].value():
            f['stead__shape__id__in'] = self['shape'].value()            
        if self['marks'].value():
            f['estate_params__id__in'] = self['marks'].value()    
        two_number_fields = {'agency_price':'agency_price', 'year_built':'bidgs__year_built',
                             'floor':'bidgs__floor', 'floor_count':'bidgs__floor_count',
                             'total_area':'bidgs__total_area', 'used_area':'bidgs__used_area',
                             'room_count':'bidgs__room_count', 'stead_area':'stead__total_area',
                             'face_area':'stead__face_area'}
        for fld, fld_name in two_number_fields.iteritems():
            if check_value_list(self[fld].value()):
                result = from_to_values(self[fld].field.clean(self[fld].value()), fld_name)
                if result: 
                    f.update(result)
        if self['wall_construcion'].value():
            f['bidgs__wall_construcion_id__in'] = self['wall_construcion'].value()            
        if check_value_list(self['created'].value()):            
            value = from_to_values(self['created'].field.clean(self['created'].value()), 'history__created')            
            if value:                 
                f.update(value)        
        if check_value_list(self['updated'].value()):            
            value = from_to_values(self['updated'].field.clean(self['updated'].value()), 'history__updated')            
            if value:                 
                f.update(value)
        if self['origin'].value():
            f['origin_id__in'] = self['origin'].value()                    
        if self['interior'].value():
            f['bidgs__interior_id__in'] = self['interior'].value()
        if self['exterior_finish'].value():
            f['bidgs__exterior_finish_id__in'] = self['exterior_finish'].value()
        if self['foto_choice'].value():
            if int(self['foto_choice'].value()) == 1:                
                f['images__id__isnull'] = False
            elif int(self['foto_choice'].value()) == 0:
                f['images__id__isnull'] = True            
        if self['description'].value():                                 
            f['description__icontains'] = self['description'].value()       
        if self['comment'].value():                                 
            f['comment__icontains'] = self['comment'].value()    
        complex_fields = ['beside', 'electricity', 'watersupply', 'gassupply', 'sewerage', 'driveway']
        lst = {}
        for fld in complex_fields:
            result = complex_field_parser(self[fld].value(), fld)
            if result: 
                lst.update(result)          
        f.update(lst)    
        return f
    class Meta:
        fieldsets = [('left', {'fields': [
                                         'validity', 'estate_status', 'estates', 'estate_category', 'estate_type',
                                         'com_status', 'region', 'locality', 'street', 'estate_number', 'room_number', 
                                         'microdistrict', 'beside', 'agency_price',
                                         ]}),
                     ('center', {'fields': [
                                            'clients', 'contacts', 'created', 'updated', 'year_built', 
                                            'floor', 'floor_count', 'wall_construcion', 'total_area', 'used_area', 
                                            'room_count', 'interior', 
                                           ]}),
                     ('right', {'fields': [
                                           'stead_area', 'face_area', 'shape', 'electricity', 'watersupply', 
                                           'gassupply', 'sewerage', 'driveway', 'origin', 'marks', 
                                           'description', 'comment', 'next', 'foto_choice' 
                                          ]})
                     ]

REGISTER_CHOICES = (
    ('outregister', 'Не в подборке'),
    ('inregister', 'В подборке'),
) 

class EstateFilterRegisterForm(EstateFilterForm):
    r_filter = forms.ChoiceField(label='', choices=REGISTER_CHOICES, widget=forms.HiddenInput())
    class Meta(EstateFilterForm.Meta):
        fieldsets = EstateFilterForm.Meta.fieldsets
        fieldsets[2][1]['fields'].append('r_filter')
    
class ContactHistoryForm(ModelForm):    
    class Meta:        
        model = ContactHistory
        widgets = {
            'event_date': DateTimeInput(attrs={'readonly':'True'}, format='%d.%m.%Y %H:%M'),
        }            

class ContactForm(ModelForm):
    class Meta:        
        fields = ('contact', 'contact_state')
        model = Contact
        
class ContactInlineForm(ContactForm):
    class Meta:
        model = Contact        

class RequiredContactFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return                
        for data in self.cleaned_data:            
            if 'DELETE' in data and not data['DELETE']:
                return  
        raise ValidationError(u'Заказчик должен иметь хотя бы один контакт!')
        
ContactFormSet = inlineformset_factory(Client, Contact, extra=1, form=ContactInlineForm, formset=RequiredContactFormSet)
ContactHistoryFormSet = inlineformset_factory(Contact, ContactHistory, extra=1, form=ContactHistoryForm)

class ObjectForm(ModelForm):
    total_area = LocalDecimalField(label=_('Total area'))
    used_area = LocalDecimalField(label=_('Used area'))
    ceiling_height = LocalDecimalField(label=_('Ceiling height'))
    year_built = LocalIntegerField(label=_('Year built'))
    floor = LocalIntegerField(label=_('Floor'))
    floor_count = LocalDecimalField(label=_('Floor count'))
    room_count = LocalIntegerField(label=_('Room count'))
    def __init__(self, *args, **kwargs):
        super(ObjectForm, self).__init__(*args, **kwargs)
        self.field_to_delete = []
        wrapper = get_wrapper(self.instance)        
        fields = wrapper.full_set            
        for field in self.fields:            
            if field not in fields:
                self.field_to_delete.append(field)                
            elif get_polymorph_label(self.instance, field):                                       
                self.fields[field].label = get_polymorph_label(self.instance, field)                           
        for field in self.field_to_delete:
            if field in self.fields:
                del self.fields[field]
        if 'appliances' in self.fields:
            self.fields['appliances'].help_text = ''                                            
        if self.instance.pk and 'documents' in self.fields:
            self.fields['documents'].queryset = Document.objects.filter(estate_type_category__id=self.instance.estate_type.estate_type_category_id)
            self.fields['documents'].help_text = ''
    estate = forms.ModelChoiceField(queryset=Estate.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = Bidg
        widgets = {
           'documents' : forms.CheckboxSelectMultiple(),
           'interior' : AutoComboboxSelectWidget(InteriorLookup),
           'appliances': AutoComboboxSelectMultipleWidget(ApplianceLookup),
        }

class BidgForm(ObjectForm):    
    def __init__(self, *args, **kwargs):
        super(BidgForm, self).__init__(*args, **kwargs)
        if self.instance.pk and 'estate_type' in self.fields:            
            self.fields['estate_type'].queryset = EstateType.objects.filter(estate_type_category__id=self.instance.estate_type.estate_type_category_id)                                                          
    class Meta(ObjectForm.Meta):
        pass        
        
class SteadForm(ObjectForm):
    total_area = LocalDecimalField(label=_('Total area'))
    face_area = LocalDecimalField(label=_('Face area'))        
    class Meta:
        model = Stead  
        widgets = {
           'documents' : forms.CheckboxSelectMultiple()        
        }
               
class LayoutForm(ModelForm):
    area = LocalDecimalField(label=_('Area'))
    class Meta:
        model = Layout  
        widgets = {
           'layout_type' : AutoComboboxSelectWidget(LayoutTypeLookup),
           'interior' : AutoComboboxSelectWidget(InteriorLookup),
        }    

LevelFormSet = inlineformset_factory(Level, Layout, extra=1, form=LayoutForm)

class LevelForm(ModelForm):
    bidg = forms.ModelChoiceField(queryset=Bidg.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = Level
        widgets = {
            'level_name' : AutoComboboxSelectWidget(LevelNameLookup),
        }   

class ImageUpdateForm(ModelForm):
    class Meta:
        model = EstatePhoto   
        fields = ('name', 'note', 'image')     

class BidForm(ModelForm):
    client = AutoCompleteSelectField(lookup_class=ClientLookup, label=u'Заказчик')    
    brokers = AutoComboboxSelectMultipleField(lookup_class=ExUserLookup, label=u'Риэлторы')
    bid_status = AutoComboboxSelectMultipleField(
            lookup_class=BidStatusLookup,
            label=_('BidStatus'),
            required=True,
        )
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['client'].widget.attrs = {'class':'long-input'}    
    class Meta:
        model = Bid    
        fields = ('client', 'brokers', 'bid_status' , 'note') 
        widgets = {
            'note': TextInput(attrs={'class': 'long-input'}) 
        }                         

class BidFilterForm(BetterForm):
    pk = AutoCompleteSelectMultipleField(
            lookup_class=BidIdLookup,
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
    created = DateRangeField(required=False, label=_('Created'))        
    updated = DateRangeField(required=False, label=_('Updated'))    
    created_by = AutoComboboxSelectField(lookup_class=ExUserLookup, label=u'Кем создано', required=False)
    broker = AutoComboboxSelectField(lookup_class=ExUserLookup, label=u'Риэлтор', required=False)    
    clients = AutoCompleteSelectMultipleField(
            lookup_class=ClientLookup,
            label=_('Client'),
            required=False,
        )
    contacts = AutoCompleteSelectMultipleField(
            lookup_class=ContactLookup,
            label=_('Contact'),
            required=False,
        )
    agency_price = IntegerRangeField(label=_('Price'), required=False)
    next = forms.CharField(required=False, widget=forms.HiddenInput(),label='')
    def get_filter(self):
        f = {}
        if self['pk'].value():
            f['id__in'] = self['pk'].value()
        if self['region'].value():
            f['regions__id__in'] = self['region'].value()
        if self['locality'].value():
            f['localities__id__in'] = self['locality'].value()
        if self['created'].value():            
            value = from_to_values(self['created'].field.clean(self['created'].value()), 'history__created')            
            if value:                 
                f.update(value)        
        if self['updated'].value():            
            value = from_to_values(self['updated'].field.clean(self['updated'].value()), 'history__updated')            
            if value:                 
                f.update(value)
        if self['created_by'].value():
            f['history__created_by_id'] = self['created_by'].value()
        if self['broker'].value():
            f['broker_id'] = self['broker'].value()
        if self['clients'].value():
            f['client__id__in'] = self['clients'].value()    
        if self['contacts'].value():
            f['client__contacts__id__in'] = self['contacts'].value()    
        if self['estate_type'].value():
            f['estate_types__id__in'] = self['estate_type'].value()   
        if check_value_list(self['agency_price'].value()):
            values = self['agency_price'].field.clean(self['agency_price'].value())                              
            if values[1]:
                f['agency_price_max__lte'] = values[1]
            if values[0]:                                                                              
                f['agency_price_min__gte'] = values[0]                                        
        return f
    class Meta:
        fieldsets = [
                     ('main', {'fields': ['pk','created', 'updated', 'created_by', 'broker', 'estate_type', 
                                          'region', 'locality', 'agency_price', 'clients', 'contacts' ,
                                          'next' ], 'legend': ''}),                    
                    ]

class EstateRegisterFilterForm(BidFilterForm):
    def __init__(self, *args, **kwargs):
        super(EstateRegisterFilterForm, self).__init__(*args, **kwargs)
        exclude = ['clients', 'contacts', 'broker']
        for field in exclude:
            del self.fields[field]        
    pk = AutoCompleteSelectMultipleField(
            lookup_class=EstateRegisterIdLookup,
            label=_('ID'),
            required=False,
        )
    name = forms.CharField(required=False, label=_('Name'))
    register_category = AutoComboboxSelectMultipleField(
            lookup_class=RegisterCategoryLookup,
            label=_('Register category'),
            required=False,
        )
        
    def get_filter(self):
        f = {}
        if self['pk'].value():
            f['id__in'] = self['pk'].value()
        if self['register_category'].value():
            f['register_category_id__in'] = self['register_category'].value()    
        if self['region'].value():
            f['bids__regions__id__in'] = self['region'].value()
        if self['locality'].value():
            f['bids__localities__id__in'] = self['locality'].value()
        if self['created'].value():            
            value = from_to_values(self['created'].field.clean(self['created'].value()), 'history__created')            
            if value:                 
                f.update(value)        
        if self['updated'].value():            
            value = from_to_values(self['updated'].field.clean(self['updated'].value()), 'history__updated')            
            if value:                 
                f.update(value)
        if self['created_by'].value():
            f['history__created_by_id'] = self['created_by'].value()
        if self['estate_type'].value():
            f['bids__estate_types__id__in'] = self['estate_type'].value()
        if self['name'].value():
            f['name__icontains'] = self['name'].value()
        if check_value_list(self['agency_price'].value()):
            values = self['agency_price'].field.clean(self['agency_price'].value())                              
            if values[1]:
                f['bids__agency_price_max__lte'] = values[1]
            if values[0]:                                                                              
                f['bids__agency_price_min__gte'] = values[0]                                
        return f
    class Meta:
        fieldsets = [
                     ('main', {'fields': ['pk','created', 'updated', 'created_by', 'name' , 'estate_type', 
                                          'region', 'locality', 'agency_price', 'next' ], 'legend': ''}),                    
                    ]

class BidPicleForm(EstateFilterForm):   
    def __init__(self, *args, **kwargs):
        super(BidPicleForm, self).__init__(*args, **kwargs)
        self.fields['estates'].label = u'Коды на осмотр'
        required_fields = []
        for field in required_fields:             
            self.fields[field].required=True
    def clean(self):        
        cleaned_data = super(BidPicleForm, self).clean()        
        region = cleaned_data.get('region')
        locality = cleaned_data.get('locality')
        agency_price = cleaned_data.get("agency_price")     
        if not agency_price or not (agency_price[0] or agency_price[1]):
            raise forms.ValidationError(u'Цена не указана')
        if not (region or locality):
            raise forms.ValidationError(u'Необходимо указать район или населенный пункт')
        if not (cleaned_data.get('estate_category') or cleaned_data.get('estate_type')):
            raise forms.ValidationError(u'Необходимо указать категорию или вид недвижимости')
        return cleaned_data    
    class Meta:        
        fieldsets = [('left', {'fields': ['num', 'estates', 'estate_category' , 'estate_type', 'region', 'locality', 'microdistrict', 'street', 'beside', 'agency_price', ], 'legend': ''}),
                     ('center', {'fields': ['year_built', 'floor', 'floor_count', 'wall_construcion', 'exterior_finish' , 'total_area', 'used_area', 'room_count', 'interior', ]}),
                     ('right', {'fields': ['stead_area', 'face_area', 'shape' , 'electricity', 'watersupply', 'gassupply', 'sewerage', 'driveway']})
                     ]

class EstateRegisterForm(BetterModelForm):      
    register_category = AutoComboboxSelectField(
            lookup_class=RegisterCategoryLookup,
            label=_('Register category'),
            required=False,
        )  
    class Meta:
        model = EstateRegister
        fieldsets = [('main', {'fields': ['bids', 'estates', 'name', 'register_category']}), ]
        widgets = {         
            'bids' : forms.MultipleHiddenInput(),
            'estates' : forms.MultipleHiddenInput()            
        }

class ClientStatusUpdateForm(ModelForm):
    class Meta:
        model = EstateClient 
        fields = ['estate_client_status']

class BidEventForm(ModelForm):
    bid_event_category = AutoComboboxSelectField(
            lookup_class=BidEventCategoryLookup,
            label = _('Event')
        )  
    class Meta:
        model = BidEvent 
        exclude = ['estates']
        widgets = {
                   'date': DateTimeInput(attrs={'class':'date-time-input'}, format='%d.%m.%Y %H:%M'),
                   'bid': forms.HiddenInput
        }
