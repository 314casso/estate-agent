from django.contrib import admin
from domanayuge.models import Category, ContentEntry, MediaLink
from categories.base import CategoryBaseAdmin
from django.contrib.contenttypes.admin import GenericTabularInline


class SimpleCategoryAdmin(CategoryBaseAdmin):
    pass


class InlineLinkEnties(GenericTabularInline):
    model = MediaLink


class ContentEntryAdmin(admin.ModelAdmin):
    list_filter = ['categories']
    inlines = [InlineLinkEnties]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, SimpleCategoryAdmin)
admin.site.register(ContentEntry, ContentEntryAdmin)
