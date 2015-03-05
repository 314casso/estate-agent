from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from devrep.models import WorkType, PartnerType, Quality, Experience, Measure,\
    Gear, Partner, PartnerClientStatus

class CustomMPTTModelAdmin(MPTTModelAdmin):    
    mptt_level_indent = 20

class ParnterAdmin(admin.ModelAdmin):
    search_fields = ['id',]
    fields = ['name', 'deleted']
    list_display = ('id', '__unicode__')
    list_filter = ('deleted',)
    def queryset(self, request):                
        return Partner.all_objects

admin.site.register(WorkType, CustomMPTTModelAdmin)
admin.site.register(PartnerType)
admin.site.register(Quality)
admin.site.register(Experience)
admin.site.register(Measure)
admin.site.register(Gear)
admin.site.register(Partner, ParnterAdmin)
admin.site.register(PartnerClientStatus)
