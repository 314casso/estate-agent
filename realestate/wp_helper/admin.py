# -*- coding: utf-8 -*-
from django.contrib import admin
from wp_helper.models import WordpressTaxonomyTree
from mptt.admin import MPTTModelAdmin
from wp_helper.service import WPService
from django import forms
from selectable.forms.widgets import AutoCompleteSelectMultipleWidget
from estatebase.lookups import EstateTypeLookup, LocalityLookup


def load_wp_taxonomy(modeladmin, request, queryset):
    wp_service = WPService()
    queryset.update(up_to_date=False)
    for taxonomy in wp_service.get_taxonomies():
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
            'estate_types': AutoCompleteSelectMultipleWidget(lookup_class=EstateTypeLookup),
            'localities': AutoCompleteSelectMultipleWidget(lookup_class=LocalityLookup),
        }
        fields = ['estate_types', 'localities']

class CustomMPTTModelAdmin(MPTTModelAdmin):
    form = TaxonomyAdminForm
    list_per_page = 50    
    mptt_level_indent = 20
    actions = [load_wp_taxonomy]
                
admin.site.register(WordpressTaxonomyTree, CustomMPTTModelAdmin)

