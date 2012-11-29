from django.contrib import admin
from migrate_app.models import SourceOrigin
from migrate_app.forms import SourceOriginForm

class SourceOriginAdmin(admin.ModelAdmin):
    form = SourceOriginForm
    def save_model(self, request, obj, form, change):
        obj.source_id = form.cleaned_data['source'].pk
        obj.save()
    
admin.site.register(SourceOrigin, SourceOriginAdmin)