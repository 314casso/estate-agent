from django.contrib import admin
from models import Region, Locality, Microdistrict, Street, Estate, EstateType, EstateTypeCategory
from django.contrib.contenttypes.models import ContentType
from realestate.orderedmodel.admin import OrderedModelAdmin

class StreetAdmin(admin.ModelAdmin):
    list_filter = ('locality',)
    raw_id_admin = ('locality',)
    search_fields = ['name',]


class EstateTypeline(admin.TabularInline):
    model = EstateType

class EstateTypeAdmin(OrderedModelAdmin):
    list_display = ['name', 'reorder']
    list_filter = ('estate_type_category',)
    raw_id_admin = ('estate_type_category',)

class EstateTypeCategoryAdmin(OrderedModelAdmin):
    list_display = ['name', 'reorder']
    inlines = [
        EstateTypeline,
    ]

admin.site.register(Region)
admin.site.register(Locality)
admin.site.register(Microdistrict)
admin.site.register(Street, StreetAdmin)
admin.site.register(ContentType)
admin.site.register(Estate)
admin.site.register(EstateType,EstateTypeAdmin)
admin.site.register(EstateTypeCategory,EstateTypeCategoryAdmin)