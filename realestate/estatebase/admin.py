from django.contrib import admin
from models import Region, Locality, Microdistrict, Street, Estate, EstateType, EstateTypeCategory
from django.contrib.contenttypes.models import ContentType

class StreetAdmin(admin.ModelAdmin):
    list_filter = ('locality',)
    raw_id_admin = ('locality',)
    search_fields = ['name',]

admin.site.register(Region)
admin.site.register(Locality)
admin.site.register(Microdistrict)
admin.site.register(Street, StreetAdmin)
admin.site.register(ContentType)
admin.site.register(Estate)
admin.site.register(EstateType)
admin.site.register(EstateTypeCategory)