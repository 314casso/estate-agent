from django.contrib import admin
from migrate_app.models import SourceOrigin, UserUser
from migrate_app.forms import SourceOriginForm, UserUserForm

class SourceOriginAdmin(admin.ModelAdmin):
    form = SourceOriginForm
    def save_model(self, request, obj, form, change):
        obj.source_id = form.cleaned_data['source'].pk
        obj.save()

class UserUserAdmin(admin.ModelAdmin):
    form = UserUserForm
    def save_model(self, request, obj, form, change):
        obj.source_id = form.cleaned_data['source'].pk
        obj.save()    
    
admin.site.register(SourceOrigin, SourceOriginAdmin)
admin.site.register(UserUser, UserUserAdmin)