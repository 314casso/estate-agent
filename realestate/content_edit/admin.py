from django.contrib import admin
from content_edit.models import CmsContent

class CmsContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'site',)
    list_filter = ('site',)
    search_fields = ('name','content')
    
admin.site.register(CmsContent, CmsContentAdmin)
