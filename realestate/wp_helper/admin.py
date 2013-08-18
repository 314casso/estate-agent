# -*- coding: utf-8 -*-
from django.contrib import admin
from wp_helper.models import WordpressTaxonomyTree, WordpressMeta,\
    WordpressMetaEstateType, WordpressMetaRegion, WordpressMetaStatus
from mptt.admin import MPTTModelAdmin
from wp_helper.service import WPService
from django import forms
from selectable.forms.widgets import AutoCompleteSelectMultipleWidget
from estatebase.lookups import LocalityLookup, EstateTypeLookup, RegionLookup,\
    EstateStatusLookup
from estatebase.models import Region, Locality, EstateType
from settings import WP_PARAMS

wp_service = WPService(WP_PARAMS['site'])

def load_wp_taxonomy(modeladmin, request, queryset):    
    queryset.update(up_to_date=False)    
    for taxonomy in wp_service.get_taxonomies():
        t = None
        try:
            t = WordpressTaxonomyTree.objects.get(wp_id=taxonomy.id)
        except WordpressTaxonomyTree.DoesNotExist:        
            WordpressTaxonomyTree.objects.create(
                                             name=taxonomy.name, 
                                             wp_id=taxonomy.id, 
                                             wp_parent_id=taxonomy.parent,
                                             up_to_date=True
                                             )
       
        if t: 
            t.name=taxonomy.name 
            t.wp_id=taxonomy.id 
            t.wp_parent_id=taxonomy.parent            
            t.up_to_date=True
            t.save()
        
            
    for taxonomy in WordpressTaxonomyTree.objects.filter(up_to_date=True):
        if taxonomy.wp_parent_id and int(taxonomy.wp_parent_id) > 0:
            taxonomy.parent = WordpressTaxonomyTree.objects.get(wp_id=taxonomy.wp_parent_id)
            taxonomy.save()    
    
    WordpressTaxonomyTree.objects.filter(up_to_date=False).delete()        
        
    WordpressTaxonomyTree.tree.rebuild()  # @UndefinedVariable
        
load_wp_taxonomy.short_description = u'Загрузить рубрики из WordPress'

class TaxonomyAdminForm(forms.ModelForm):    
    class Meta(object):        
        model = WordpressTaxonomyTree        
        widgets = {            
            'localities': AutoCompleteSelectMultipleWidget(lookup_class=LocalityLookup),
        }
        fields = ['localities', 'wp_meta_locality', 'regions']

class MetaAdminForm(forms.ModelForm):    
    class Meta(object):        
        model = WordpressMeta
        fields = ['name']

class WordpressMetaEstateTypeAdminForm(forms.ModelForm):
    class Meta(object):        
        model = WordpressMetaEstateType        
        widgets = {            
            'estate_types': AutoCompleteSelectMultipleWidget(lookup_class=EstateTypeLookup),
        }
        fields = ['name','estate_types','wp_id']

class WordpressMetaEstateTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'wp_id')
    form = WordpressMetaEstateTypeAdminForm
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['unlinked_objects'] = ', '.join(EstateType.objects.filter(wp_taxons=None).values_list('name',flat=True))
        return super(WordpressMetaEstateTypeAdmin, self).changelist_view(request, extra_context=extra_context)

class WordpressMetaRegionAdminForm(forms.ModelForm):
    list_display = ('name', 'wp_id')
    class Meta(object):        
        model = WordpressMetaRegion        
        widgets = {            
            'regions': AutoCompleteSelectMultipleWidget(lookup_class=RegionLookup),
        }
        fields = ['name','regions','wp_id']

class WordpressMetaStatusAdminForm(forms.ModelForm):
    class Meta(object):        
        model = WordpressMetaStatus        
        widgets = {            
            'estate_statuses': AutoCompleteSelectMultipleWidget(lookup_class=EstateStatusLookup),
        }
        fields = ['name','estate_statuses', 'wp_id']

class WordpressMetaRegionAdmin(admin.ModelAdmin):
    form = WordpressMetaRegionAdminForm
    list_display = ('name', 'wp_id')

class WordpressMetaStatusAdmin(admin.ModelAdmin):
    form = WordpressMetaStatusAdminForm
    list_display = ('name', 'wp_id')

def clear_localities(modeladmin, request, queryset):
    for t in WordpressTaxonomyTree.objects.all():
        t.localities.clear()
        
def set_localities(modeladmin, request, queryset):    
    for region in Region.objects.all():
        q = WordpressTaxonomyTree.objects.filter(level__lte=2, parent__regions__id=region.id)
        for locality in Locality.objects.filter(region=region, wp_taxons=None):            
            taxonomy_item = wp_service.find_term(locality.name, q)
            if taxonomy_item:
                taxonomy_item.localities.add(locality)
            else:
                print '%s not found!' % locality

set_localities.short_description = u'Найти соответствия рубрик и населенных пунктов'

def set_meta_localities(modeladmin, request, queryset):    
    q = WordpressTaxonomyTree.objects.filter(level__lte=2)
    for locality in WordpressMeta.objects.all():            
        taxonomy_item = wp_service.find_term(locality.name, q)
        if taxonomy_item:
            taxonomy_item.wp_meta_locality = locality
            taxonomy_item.save()
        else:
            print '%s not found!' % locality

set_meta_localities.short_description = u'Найти соответствия рубрик и жестких полей'


class CustomMPTTModelAdmin(MPTTModelAdmin):
    change_list_template = 'mptt_change_list.html'
    form = TaxonomyAdminForm
    list_per_page = 50    
    mptt_level_indent = 20
    actions = [load_wp_taxonomy, set_localities, set_meta_localities]
    def locality(self, obj):
        return ', '.join(obj.localities.values_list('name',flat=True))
    def queryset(self, request):        
        qs = super(CustomMPTTModelAdmin, self).queryset(request)        
        return qs.filter(level__lte=2)
    def wp_meta_locality_blank(self, obj):
        return obj.wp_meta_locality or ''
    wp_meta_locality_blank.short_description = u'Жесткое поле'
    list_display = ('name', 'locality', 'wp_meta_locality_blank')    
    search_fields = ['name']
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['unlinked_localities'] = ', '.join(Locality.objects.filter(wp_taxons=None).values_list('name',flat=True)) 
        extra_context['unlinked_regions'] = ', '.join(Region.objects.filter(wp_taxons=None).values_list('name',flat=True))
        extra_context['unlinked_meta'] = ', '.join(WordpressMeta.objects.filter(wp_taxon=None).values_list('name',flat=True))
        return super(CustomMPTTModelAdmin, self).changelist_view(request, extra_context=extra_context)

class WordpressMetaAdmin(admin.ModelAdmin): 
    list_display = ('name', 'wp_id')
    form = MetaAdminForm   
    search_fields = ['name']
    
admin.site.register(WordpressTaxonomyTree, CustomMPTTModelAdmin)
admin.site.register(WordpressMeta, WordpressMetaAdmin)
admin.site.register(WordpressMetaEstateType, WordpressMetaEstateTypeAdmin)
admin.site.register(WordpressMetaRegion, WordpressMetaRegionAdmin)
admin.site.register(WordpressMetaStatus, WordpressMetaStatusAdmin)