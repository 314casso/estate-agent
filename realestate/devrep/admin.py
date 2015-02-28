from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from devrep.models import WorkType, PartnerType, Quality, Experience, Measure,\
    Gear

class CustomMPTTModelAdmin(MPTTModelAdmin):    
    mptt_level_indent = 20

admin.site.register(WorkType, CustomMPTTModelAdmin)
admin.site.register(PartnerType)
admin.site.register(Quality)
admin.site.register(Experience)
admin.site.register(Measure)
admin.site.register(Gear)
