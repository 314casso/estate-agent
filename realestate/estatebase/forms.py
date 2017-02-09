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
    complex_field_parser, check_value_list, history_filter, from_to
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
    RegisterCategoryLookup, ExteriorFinishLookup, BidStatusLookup,\
    OutbuildingLookup, PurposeLookup, HeatingLookup, YandexBuildingLookup,\
    DealStatusLookup, BidStatusCategoryLookup
from estatebase.models import Client, Contact, ContactHistory, Bidg, Estate, \
    Document, Layout, Level, EstatePhoto, Stead, Bid, EstateRegister, \
    EstateType, EstateClient, BidEvent, EntranceEstate,\
    EstateFile, GenericLink, BidStatusCategory
from estatebase.wrapper import get_polymorph_label, get_wrapper
from form_utils.forms import BetterForm, BetterModelForm
from selectable.forms import AutoCompleteSelectWidget
from selectable.forms.fields import AutoCompleteSelectMultipleField, \
    AutoCompleteSelectField
from selectable.forms.widgets import AutoComboboxSelectWidget,\
    AutoComboboxSelectMultipleWidget
from settings import CORRECT_DELTA
from django.utils.safestring import mark_safe
from django.template.base import Template
from django.core.exceptions import ValidationError
from exportdata.utils import EstateTypeMapper
from devrep.lookups import WorkTypeLookup, GoodsLookup, PartnerLookup,\
    ExperienceLookup, QualityLookup, DevProfileIdLookup 
from wp_helper.models import EstateWordpressMeta
from django.contrib.contenttypes.forms import generic_inlineformset_factory


class EstateForm(BetterModelForm):             
    agency_price = LocalIntegerField(label=_('Agency price'))
    saler_price = LocalIntegerField(label=_('Saler price'))

    def __init__(self, *args, **kwargs):
        super(EstateForm, self).__init__(*args, **kwargs)        
        exclude = ['address_state',]
        _user = self.initial.get('_user')
        su = _user and _user.is_superuser
        if not su:         
            for field in exclude:
                del self.fields[field]
        manager_fields = ['broker',]
        if not _user or not _user.has_perm('estatebase.change_broker'):
            for field in manager_fields:
                self.fields[field].widget = forms.widgets.HiddenInput()
        
    def clean_estate_number(self):
        data = self.cleaned_data['estate_number']
        data = data.strip()            
        if data == '0':
            raise forms.ValidationError(u'"0" не является верным номером лота')
        return data 
    
    def clean_street(self):
        data = self.cleaned_data['street']                            
        if data is not None and data.name.lower() == u'не присвоено':
            raise forms.ValidationError(u'"не присвоено" не является верной улицей')
        return data
                
    class Meta:                
        model = Estate
        fields = ('origin', 'region', 'locality', 'microdistrict', 'street', 'estate_number', 
                  'saler_price', 'agency_price', 'estate_status', 'broker', 'com_status', 'deal_status', 'address_state')
        widgets = {
            'estate_status': AutoComboboxSelectWidget(EstateStatusLookup),            
            'region': AutoComboboxSelectWidget(RegionLookup),
            'origin': AutoComboboxSelectWidget(OriginLookup),
            'street': AutoCompleteSelectWidget(StreetLookup),
            'locality': AutoComboboxSelectWidget(LocalityLookup),
            'microdistrict' : AutoComboboxSelectWidget(MicrodistrictLookup),
            'broker': AutoComboboxSelectWidget(ExUserLookup),
            'com_status': AutoComboboxSelectWidget(ComChoiceLookup),
            'deal_status': AutoComboboxSelectWidget(DealStatusLookup),           
        }

class EstateCreateForm(EstateForm):
    estate_category_filter = AutoCompleteSelectField(widget=AutoComboboxSelectWidget, 
            lookup_class=EstateTypeCategoryLookup,
            label=_('EstateTypeCategory'),
            required=False
        )
    estate_type = AutoCompleteSelectField(widget=AutoComboboxSelectWidget, 
            lookup_class=EstateTypeLookup,
            label=_('Estate type')
        )
    class Meta(EstateForm.Meta):        
        fields = ('estate_category_filter', 'estate_type', 'origin', 'region', 'locality', 'microdistrict', 'street', 'estate_number', 
                  'beside', 'beside_distance', 'saler_price', 'agency_price', 'estate_status', 'estate_type', 'broker', 'com_status', 'deal_status', 'address_state')

class EstateCreateClientForm(EstateCreateForm):
    client_status = AutoCompleteSelectField(widget=AutoComboboxSelectWidget, lookup_class=EstateClientStatusLookup, label=_('Estate client status'))
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
                  'beside', 'beside_distance', 'saler_price', 'agency_price', 'estate_status', 'estate_type', 'broker', 'com_status', 'deal_status', 'address_state')

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
                    'electricity_distance':TextInput(attrs={'class':'local-int-f'}), 
                    'watersupply_distance':TextInput(attrs={'class':'local-int-f'}),
                    'gassupply_distance':TextInput(attrs={'class':'local-int-f'}),
                    'sewerage_distance':TextInput(attrs={'class':'local-int-f'}),
                    'driveway_distance':TextInput(attrs={'class':'local-int-f'}),
                  }

class EstateParamForm(ModelForm):
    class Meta:                
        model = Estate
        fields = ('estate_params', 'description', 'client_description' , 'comment')
        widgets = {
           'estate_params' : forms.CheckboxSelectMultiple()        
        }

class ClientForm(ModelForm):   
    origin = AutoCompleteSelectField(widget=AutoComboboxSelectWidget, 
            lookup_class=OriginLookup,
            label=_('Origin'),
            required=False,
        )  
    class Meta:        
#        exclude = ('created_by', 'updated', 'created', 'updated_by', 'deleted')
        fields = ['origin','client_type', 'has_dev_profile', 'name', 'address', 'note', ]
        
        model = Client
        widgets = {
            'note': Textarea(attrs={'rows':'5'}),
            'address' : TextInput(attrs={'class': 'big-text-input'}),
            'created' : DateTimeInput(attrs={'readonly':'True'}, format='%d.%m.%Y %H:%M'),
            'valid' : CheckboxInput(attrs={'disabled':'disabled'}),            
        }

class ClientFilterForm(BetterForm):
    pk = AutoCompleteSelectMultipleField(
            lookup_class=ClientIdLookup,
            label=_('ID'),
            required=False            
        )
    created = DateRangeField(required=False, label=_('Created'))
    created_by = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=ExUserLookup, label=u'Кем создано', required=False)       
    updated = DateRangeField(required=False, label=_('Updated'))
    updated_by = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=ExUserLookup, label=u'Кем обновлено', required=False)
    origin = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=OriginLookup,
            label=_('Origin'),
            required=False,
        )
    client_type = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=ClientTypeLookup,
            label=_('ClientType'),
            required=False,
        )
        
    DEV_PROFILE_CHOICES = ((3, u'Неважно',), (0, u'Нет',), (1, u'Да',))
    has_dev_profile = forms.ChoiceField(label=_('HasDevProfile'), widget=forms.RadioSelect, choices=DEV_PROFILE_CHOICES, initial=3, required=False,)
    
    name = forms.CharField(required=False, label=_('Name'))
    address = forms.CharField(required=False, label=_('Address'))
    contacts = AutoCompleteSelectMultipleField(
            lookup_class=ContactLookup,
            label=_('Contact'),
            required=False,
        )
    note = forms.CharField(required=False, label=_('Note'))
    fio = forms.CharField(required=False, label=u'Ф.И.О.')
    next = forms.CharField(required=False, widget=forms.HiddenInput())
    
    work_types = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=WorkTypeLookup,
            label=_('WorkType'),
            required=False,
        )
    
    goods = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=GoodsLookup,
            label=_('Goods'),
            required=False,
        )
    
    partners = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=PartnerLookup,
            label=_('Partners'),
            required=False,
        ) 
    
    birthday = DateRangeField(required=False, label=_('Birthday'))
    
    experience = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=ExperienceLookup,
            label=_('Experience'),
            required=False,
        )
    
    quality = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=QualityLookup,
            label=_('Quality'),
            required=False,
        )
    
    coverage_regions = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=RegionLookup,
            label=_('Regions'),
            required=False,
        )
    
    coverage_localities = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=LocalityLookup,
            label=_('Localities'),
            required=False,
        )
    
    dev_profiles = AutoCompleteSelectMultipleField(
            lookup_class=DevProfileIdLookup,
            label=_('DevProfile'),
            required=False,
        )  
    
    dev_note = forms.CharField(required=False, label=u'Примечание строителя')
    
    def get_filter(self):
        if self.is_valid():
            return self.make_filter(self.cleaned_data)
        return {}
            
    def make_filter(self, cleaned_data):
        f = {}
        if not cleaned_data:
            return f   
        
        q = Q()
        fio = cleaned_data['fio']
        if fio:
            parts = fio.split()
            for part in parts:                
                q = q | Q(extra_profile__last_name__icontains=part) | Q(extra_profile__first_name__icontains=part) | Q(extra_profile__patronymic__icontains=part) 
        
        address = cleaned_data['address']
        if address:
            parts = address.split()
            for part in parts:
                q = q | Q(extra_profile__address__address__icontains=part) | Q(extra_profile__address__region__icontains=part) | Q(extra_profile__address__locality__icontains=part)
                q = q | Q(address__icontains=part)
        
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
                          'contacts__in': 'contacts',
                          'name__icontains': 'name',
                          'client_type__in': 'client_type',
                          'origin__in': 'origin',                          
                          'note__icontains': 'note',
                          'dev_profile__work_types__in': 'work_types',
                          'dev_profile__goods__in': 'goods',
                          'dev_profile__client__partner__in' : 'partners',
                          'dev_profile__experience__in': 'experience',
                          'dev_profile__quality__in': 'quality',
                          'dev_profile__coverage_regions__in': 'coverage_regions', 
                          'dev_profile__coverage_localities__in': 'coverage_localities', 
                          'dev_profile__note__icontains': 'dev_note',
                          'dev_profile__in': 'dev_profiles',
                         }
        
        two_number_fields = {'birthday':'extra_profile__birthday'}
        
        for fld, fld_name in two_number_fields.iteritems():
            if check_value_list(cleaned_data[fld]):
                result = from_to_values(cleaned_data[fld], fld_name)
                if result: 
                    f.update(result)
        
        for key, value in simple_filter.iteritems():
            if value in cleaned_data and cleaned_data[value]:                
                f[key] = cleaned_data[value]
        
        has_dev_profile = cleaned_data['has_dev_profile']
        has_dev_profile = int(has_dev_profile) if has_dev_profile else 3
        if has_dev_profile < 3:            
            f['has_dev_profile__exact'] = has_dev_profile == 1        
        return f
    class Meta:
        fieldsets = [('basic', {'fields': [
                                         'pk','created','created_by','updated','updated_by','origin','client_type',
                                         'has_dev_profile','name','fio','birthday','address','contacts','note','next'
                                         ]}),
                     ('devrep', {'fields': [
                                         'dev_profiles', 'work_types','goods','partners','experience','quality','coverage_regions',
                                         'coverage_localities','dev_note'
                                           ]}),                     
                     ]
           
               
class EstateFilterForm(BetterForm):
    _filter_by_pk = True    
    validity = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=ValidityLookup,
            label=_('Validity'),
            required=False,
        )    
    estates = AutoCompleteSelectMultipleField(
            lookup_class=EstateLookup,
            label=_('ID'),
            required=False,
        )
    estate_category = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=EstateTypeCategoryLookup,
            label=_('EstateTypeCategory'),
            required=False,
        )
    estate_type = AutoCompleteSelectMultipleField(
            lookup_class=EstateTypeLookup,
            label=_('Estate type'),
            required=False,
        )
    outbuildings = AutoCompleteSelectMultipleField(
            lookup_class=OutbuildingLookup,
            label=_('Outbuildings'),
            required=False,
        ) 
    com_status = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=ComChoiceLookup,
            label=_('Commerce'),
            required=False,
        ) 
    region = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=RegionLookup,
            label=_('Region'),
            required=False,
        )    
    locality = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
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
    estate_status = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
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
    wall_construcion = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=WallConstrucionLookup,
            label=_('Wall Construcion'),
            required=False,
        )
    total_area = DecimalRangeField(required=False, label=_('Total area'))
    used_area = DecimalRangeField(required=False, label=_('Used area'))   
    room_count = IntegerRangeField(required=False, label=_('Room count'))
    stead_area = DecimalRangeField(required=False, label=_('Stead area'))
    
    created = DateRangeField(required=False, label=_('Created'))
    created_by = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=ExUserLookup, label=u'Кем создано', required=False)        
    updated = DateRangeField(required=False, label=_('Updated'))
    updated_by = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=ExUserLookup, label=u'Кем обновлено', required=False)
    origin = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=OriginLookup,
            label=_('Origin'),
            required=False,
        )  
    beside = ComplexField(required=False, label=_('Beside'), lookup_class=BesideLookup)
    beside_type = forms.ChoiceField(label=u'Тип выхода/вида', choices=(('','------'),) + EntranceEstate.TYPE_CHOICES, required=False, initial='')
    interior = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=InteriorLookup,
            label=_('Interior'),
            required=False,
        )
    exterior_finish = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=ExteriorFinishLookup,
            label=_('Exterior finish'),
            required=False,
        )    
    face_area = DecimalRangeField(required=False, label=_('Face area'))
    shape = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=ShapeLookup,
            label=_('Shape'),
            required=False,
        ) 
    electricity = ComplexField(required=False, label=_('Electricity'), lookup_class=ElectricityLookup)
    watersupply = ComplexField(required=False, label=_('Watersupply'), lookup_class=WatersupplyLookup)    
    gassupply = ComplexField(required=False, label=_('Gassupply'), lookup_class=GassupplyLookup)    
    sewerage = ComplexField(required=False, label=_('Sewerage'), lookup_class=SewerageLookup)
    driveway = ComplexField(required=False, label=_('Driveway'), lookup_class=DrivewayLookup)
    
    marks = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=EstateParamLookup,
            label=_('Estate params'),
            required=False,
        ) 
    
    FOTO_CHOICES = ((3, u'Все',), (0, u'Нет фото',), (1, u'Есть фото',))
    foto_choice = forms.ChoiceField(label=_('EstatePhoto'), widget=forms.RadioSelect, choices=FOTO_CHOICES, initial=3, required=False,)
    WP_CHOICES = ((3, u'Все',), (0, u'Не размещено',), (1, u'Размещено',))
    wp_choice = forms.ChoiceField(label=u'Сайт', widget=forms.RadioSelect, choices=WP_CHOICES, initial=3, required=False,)
    description = forms.CharField(required=False, label=_('Description'))
    comment = forms.CharField(required=False, label=_('Comment'))
    broker = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=ExUserLookup, label=u'Риэлтор', required=False)
    purposes = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=PurposeLookup, label=_('Purpose'), required=False)
    layouts = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=LayoutTypeLookup, label=_('Layout type'), required=False)
    heating = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=HeatingLookup, label=_('Heating'), required=False)
    next = forms.CharField(required=False, widget=forms.HiddenInput())
    cadastral_number = forms.CharField(required=False, label=_('Cadastral number'))
    client_description = forms.CharField(required=False, label=_('Client description'))
    wp_status = forms.ChoiceField(required=False, label=u'Статус на сайте', initial='')
    layout_area = DecimalRangeField(required=False, label=_('Area'))
    address_state = forms.ChoiceField(label=_('Address state'), choices=(('','------'),) + Estate.ADDRESS_CHOICES, required=False,)
    def __init__(self, *args, **kwargs):
        super(EstateFilterForm, self).__init__(*args, **kwargs)
        self.fields['next'].label = ''         
        self.fields['wp_status'].choices = [('', '------')] + list(EstateWordpressMeta.STATE_CHOICES)
    def type_filter(self, cleaned_data):
        if not cleaned_data:
            return
        q = Q()        
        cats = cleaned_data['estate_category']       
        types = cleaned_data['estate_type']        
        for t in types:
            if t.estate_type_category in cats:
                cats.remove(t.estate_type_category)
            q = q | Q(bidgs__estate_type_id__exact=t.pk, estate_category_id__exact=t.estate_type_category_id)
            q = q | Q(stead__estate_type_id__exact=t.pk, estate_category_id__exact=t.estate_type_category_id)
        if len(cats):
            q = q | Q(estate_category__in=cats)
        return q
    
    def get_filter(self):
        if self.is_valid():
            return self.make_filter(self.cleaned_data)
        return {}
    
    def make_filter(self, cleaned_data):
        f = {}
        if not cleaned_data:
            return f                     
        q = self.type_filter(cleaned_data)        
        if len(q):
            f['Q'] = q   
        
        if cleaned_data['validity']:
            ids = set(validity.id for validity in cleaned_data['validity'])
            if Estate.EXPIRED in ids:                                
                ids.add(Estate.VALID)
            f['validity__in'] = ids
            if Estate.EXPIRED in ids:
                f['history__modificated__lte'] = CORRECT_DELTA
            elif Estate.VALID in ids:
                f['history__modificated__gt'] = CORRECT_DELTA
        
        if cleaned_data['estates'] and self._filter_by_pk:
            f['id__in'] = [item.pk for item in cleaned_data['estates']] 
        
        if cleaned_data['estate_number']:                                 
            f['estate_number__icontains'] = cleaned_data['estate_number']
                    
        simple_filter = {'com_status__in': 'com_status', 'region__in': 'region',
                         'locality__in': 'locality', 'microdistrict__in': 'microdistrict',
                         'street__in': 'street', 'bidgs__room_number__icontains': 'room_number',
                         'estate_status__in': 'estate_status', 'clients__in': 'clients',
                         'clients__contacts__in': 'contacts', 'stead__shape__in': 'shape',
                         'estate_params__in': 'marks', 'bidgs__wall_construcion__in': 'wall_construcion',
                         'origin__in': 'origin', 'bidgs__interior__in': 'interior',
                         'bidgs__exterior_finish__in': 'exterior_finish', 'description__icontains': 'description',
                         'comment__icontains': 'comment','bidgs__estate_type_id__in' :'outbuildings',
                         'broker__in' : 'broker', 'stead__purpose__in' : 'purposes', 
                         'bidgs__levels__layout__layout_type__in' : 'layouts', 
                         'history__created_by__in': 'created_by', 'history__updated_by__in': 'updated_by',
                         'bidgs__heating__in':'heating', 'stead__cadastral_number__icontains': 'cadastral_number',
                         'client_description__icontains': 'client_description',
                         'wp_meta__status':'wp_status', 'address_state__in': 'address_state'                       
                         }
        
        for key, value in simple_filter.iteritems():
            if value in cleaned_data and cleaned_data[value]:                
                f[key] = cleaned_data[value]  
                
        two_number_fields = {'agency_price':'agency_price', 'year_built':'bidgs__year_built',
                             'floor':'bidgs__floor', 'floor_count':'bidgs__floor_count',
                             'total_area':'bidgs__total_area', 'used_area':'bidgs__used_area',
                             'room_count':'bidgs__room_count', 'stead_area':'stead__total_area',
                             'face_area':'stead__face_area','layout_area': 'bidgs__levels__layout__area'}
        for fld, fld_name in two_number_fields.iteritems():
            if check_value_list(cleaned_data[fld]):
                result = from_to_values(cleaned_data[fld], fld_name)
                if result: 
                    f.update(result)
               
        history_fields = ('created','updated')
        for fld in history_fields:
            cleaned_value = cleaned_data[fld]
            if cleaned_value:
                value = history_filter(cleaned_value, fld)
                if value:                 
                    f.update(value)
        
        choice_fields = {'foto_choice':'images__isnull', 'wp_choice':'wp_meta__post_id__isnull'}
        for key, value in choice_fields.iteritems():
            if cleaned_data[key] and int(cleaned_data[key]) < 3:                
                f[value] = int(cleaned_data[key]) == 0
            
        complex_fields = ['electricity', 'watersupply', 'gassupply', 'sewerage', 'driveway']
        lst = {}
        for fld in complex_fields:
            result = complex_field_parser(cleaned_data[fld], fld)
            if result: 
                lst.update(result)          
        f.update(lst)    
        
        if cleaned_data['beside_type']:
            f.update({'entranceestate_set__type': cleaned_data['beside_type']})            
        
        if cleaned_data['beside'][0]:
            f.update({'%s__exact' % 'entrances' : cleaned_data['beside'][0]})
            if cleaned_data['beside'][1]:
                num = from_to(cleaned_data['beside'][1], 'entranceestate_set__distance')
                if num:
                    f.update(num)
        return f    
    
    class Meta:
        fieldsets = [('left', {'fields': [
                                         'validity', 'estate_status', 'estates', 'estate_category', 'estate_type',
                                         'com_status', 'region', 'locality', 'street', 'estate_number', 'room_number', 
                                         'microdistrict', 'address_state', 'beside_type', 'beside', 'agency_price', 'wp_choice','wp_status',
                                         ]}),
                     ('center', {'fields': [
                                            'clients', 'client_description', 'contacts', 'created', 'created_by', 'updated', 'updated_by', 'year_built', 
                                            'floor', 'floor_count', 'wall_construcion', 'total_area', 'used_area', 
                                            'room_count', 'interior', 'heating', 'layouts', 'layout_area', 'outbuildings', 'broker'
                                           ]}),
                     ('right', {'fields': [
                                           'stead_area', 'face_area', 'shape', 'cadastral_number', 'purposes', 'electricity', 'watersupply', 
                                           'gassupply', 'sewerage', 'driveway', 'origin', 'marks', 
                                           'description', 'comment', 'next', 'foto_choice',
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
        fields = '__all__'
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
        fields = '__all__'
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
        fields = '__all__'
        widgets = {
           'documents' : forms.CheckboxSelectMultiple(),
           'interior' : AutoComboboxSelectWidget(InteriorLookup),
           'appliances': AutoComboboxSelectMultipleWidget(ApplianceLookup),
           'yandex_building':AutoComboboxSelectWidget(YandexBuildingLookup), 
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
    def __init__(self, *args, **kwargs):
        super(SteadForm, self).__init__(*args, **kwargs)
        if self.instance.pk and 'estate_type' in self.fields:            
            self.fields['estate_type'].queryset = EstateType.objects.filter(estate_type_category__id=self.instance.estate_type.estate_type_category_id)         
    def clean_total_area(self):        
        data = self.cleaned_data['total_area']
        if self.user is None:
            raise forms.ValidationError(u'Текущий пользователь не определен!')
        if self.user.is_superuser:
            return data            
        if not data:
            raise forms.ValidationError(u'Значение не оставаться пустым!')
        validate_map = {
                            EstateTypeMapper.DOM: 101,
                            EstateTypeMapper.DACHA: 15,
                            EstateTypeMapper.DACHNYYUCHASTOK: 60,
                            EstateTypeMapper.TAUNHAUS:30,
                            EstateTypeMapper.UCHASTOKKOMMERCHESKOGONAZNACHENIYA: 101,
                            EstateTypeMapper.UCHASTOKDLYASTROITELSTVADOMA: 101,
                            EstateTypeMapper.UCHASTOKSELSKOHOZYAYSTVENNOGONAZNACHENIYA: 5000,
                            EstateTypeMapper.KVARTIRASUCHASTKOM: 50,
                            EstateTypeMapper.GARAZH: 15,
                            EstateTypeMapper.ZHILOYGARAZH:15,
                            EstateTypeMapper.LODOCHNYYGARAZH:15,
                            EstateTypeMapper.BATALERKA:15,
                        }
        min_value = validate_map.get(self.instance.estate_type_id)
        if data < min_value:
            raise forms.ValidationError(u'Указанное значение %s кв.м меньше минимально возможного %s кв.м' % (data, min_value))
        return data
                
    class Meta:
        fields = '__all__'
        model = Stead  
        widgets = {
          'documents' : forms.CheckboxSelectMultiple()        
        }        
               
class LayoutForm(ModelForm):
    area = LocalDecimalField(label=_('Area'))
    class Meta:
        fields = '__all__'
        model = Layout  
        widgets = {
           'layout_type' : AutoComboboxSelectWidget(LayoutTypeLookup),
           'interior' : AutoComboboxSelectWidget(InteriorLookup),
        }    

LevelFormSet = inlineformset_factory(Level, Layout, extra=1, form=LayoutForm)

class LevelForm(ModelForm):
    bidg = forms.ModelChoiceField(queryset=Bidg.objects.all(), widget=forms.HiddenInput())
    class Meta:
        fields = '__all__'
        model = Level
        widgets = {
            'level_name' : AutoComboboxSelectWidget(LevelNameLookup),
        }   

class ImageUpdateForm(ModelForm):
    class Meta:
        model = EstatePhoto   
        fields = ('name', 'note', 'image')     

class FileUpdateForm(ModelForm):
    class Meta:
        model = EstateFile   
        fields = ('name', 'note', 'file')

class BidForm(ModelForm):
    client = AutoCompleteSelectField(lookup_class=ClientLookup, label=u'Заказчик')    
    brokers = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=ExUserLookup, label=u'Риэлторы')
    bid_status = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
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
            'note': Textarea() 
        }                         

class BidUpdateForm(ModelForm):
    brokers = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=ExUserLookup, label=u'Риэлторы')
    bid_status = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=BidStatusLookup,
            label=_('BidStatus'),
            required=True,
        )    
    class Meta():            
        fields = ('brokers', 'bid_status' , 'note')
        model = Bid    
        widgets = {
            'note': Textarea() 
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
    region = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=RegionLookup,
            label=_('Region'),
            required=False,
        )    
    locality = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=LocalityLookup,
            label=_('Locality'),
            required=False,
        )
    estates = AutoCompleteSelectMultipleField(
            lookup_class=EstateLookup,
            label=u'Коды на осмотр',
            required=False,
        )
    created = DateRangeField(required=False, label=_('Created'))        
    updated = DateRangeField(required=False, label=_('Updated'))    
    created_by = AutoCompleteSelectField(widget=AutoComboboxSelectWidget, lookup_class=ExUserLookup, label=u'Кем создано', required=False)
    updated_by = AutoCompleteSelectField(widget=AutoComboboxSelectWidget, lookup_class=ExUserLookup, label=u'Кем обновлено', required=False)
    broker = AutoCompleteSelectField(widget=AutoComboboxSelectWidget, lookup_class=ExUserLookup, label=u'Риэлтор', required=False)    
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
    origin = AutoCompleteSelectField(widget=AutoComboboxSelectWidget, 
            lookup_class=OriginLookup,
            label=_('Origin'),
            required=False,
        )      
    bid_status = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=BidStatusLookup,
            label=_('BidStatus'),
            required=False,
        )
    
    category = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
            lookup_class=BidStatusCategoryLookup,
            label=_('BidStatusCategory'),
            required=False,
        )
        
    agency_price = IntegerRangeField(label=_('Price'), required=False)
    bid_event_category = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, lookup_class=BidEventCategoryLookup, label=_('BidEventCategory'), required=False)
    date_event = DateRangeField(required=False, label=_('Event date'))
    note = forms.CharField(required=False, label=_('Note'))    
    next = forms.CharField(required=False, widget=forms.HiddenInput(),label='')
    def get_filter(self):
        f = {}
        if self['pk'].value():
            f['id__in'] = self['pk'].value()
        if self['region'].value():
            #f['regions__id__in'] = self['region'].value()
            q = Q(regions__id__in=self['region'].value()) | Q(localities__region__id__in=self['region'].value())
            f['Q'] = q
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
        if self['updated_by'].value():
            f['history__updated_by_id'] = self['updated_by'].value()
        if self['broker'].value():
            f['brokers__id'] = self['broker'].value()
        if self['origin'].value():
            f['client__origin__id'] = self['origin'].value()    
        if self['clients'].value():
            f['clients__id__in'] = self['clients'].value()    
        if self['contacts'].value():
            f['clients__contacts__id__in'] = self['contacts'].value()
        
        if self['category'].value():
            f['bid_status__category__id__in'] = self['category'].value()
                            
        if self['bid_status'].value():
            f['bid_status__id__in'] = self['bid_status'].value()         
        if self['estates'].value():
            f['estates__id__in'] = self['estates'].value()            
        if self['estate_type'].value():
            f['estate_types__id__in'] = self['estate_type'].value()
        if self['bid_event_category'].value():
            f['bid_events__bid_event_category_id__in'] = self['bid_event_category'].value()
        if self['note'].value():
            f['note__icontains'] = self['note'].value()
        if self['date_event'].value():            
            value = from_to_values(self['date_event'].field.clean(self['date_event'].value()), 'bid_events__date')            
            if value:                 
                f.update(value)    
        if check_value_list(self['agency_price'].value()):
            values = self['agency_price'].field.clean(self['agency_price'].value())                              
            if values[1]:
                f['agency_price_max__lte'] = values[1]
            if values[0]:                                                                              
                f['agency_price_min__gte'] = values[0]                                        
        return f
    class Meta:
        fieldsets = [
                     ('main', {'fields': ['pk','created', 'updated', 'created_by', 'updated_by', 'broker', 'category', 'bid_status', 
                                          'origin', 'estate_type', 'estates', 
                                          'region', 'locality', 'agency_price', 'clients', 'contacts' ,
                                          'bid_event_category', 'date_event', 'note',
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
    register_category = AutoCompleteSelectMultipleField(widget=AutoComboboxSelectMultipleWidget, 
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
    _filter_by_pk = False
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
        fieldsets = [('left', {'fields': ['num', 'estates', 'estate_category' , 'estate_type', 'com_status', 'region', 'locality', 'microdistrict', 'street', 'beside_type', 'beside', 'agency_price', ], 'legend': ''}),
                     ('center', {'fields': ['year_built', 'floor', 'floor_count', 'wall_construcion', 'exterior_finish' , 'total_area', 'used_area', 'room_count', 'interior', 'layouts', 'layout_area', 'outbuildings']}),
                     ('right', {'fields': ['stead_area', 'face_area', 'shape', 'purposes', 'electricity', 'watersupply', 'gassupply', 'sewerage', 'driveway']})
                     ]

class EstateRegisterForm(BetterModelForm):      
    register_category = AutoCompleteSelectField(widget=AutoComboboxSelectWidget, 
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
    bid_event_category = AutoCompleteSelectField(widget=AutoComboboxSelectWidget, 
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


class EntranceEstateInlineForm(ModelForm):        
    class Meta:
        model = EntranceEstate
        fields = ['beside', 'type', 'distance', 'basic']
        widgets = {
                  'beside':AutoComboboxSelectWidget(BesideLookup),
                  'distance':TextInput(attrs={'class':'local-int-f'}), 
                   }


EntranceEstateFormSet = inlineformset_factory(Estate, EntranceEstate, extra=1, form=EntranceEstateInlineForm)

GenericLinkFormset = generic_inlineformset_factory(GenericLink, extra=1,)
