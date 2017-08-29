from django.contrib import admin
from domanayuge.models import Category, ContentEntry, MediaLink, LocalityDomain,\
    SiteMeta, MetaTag
from categories.base import CategoryBaseAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.admin.options import TabularInline


class SimpleCategoryAdmin(CategoryBaseAdmin):
    pass


class InlineLinkEnties(GenericTabularInline):
    model = MediaLink

class InlineMetaTags(TabularInline):
    model = MetaTag

class ContentEntryAdmin(admin.ModelAdmin):
    list_filter = ['categories']
    inlines = [InlineLinkEnties]
    prepopulated_fields = {"slug": ("title",)}


class LocalityDomainAdmin(admin.ModelAdmin):
    pass

class SiteMetaAdmin(admin.ModelAdmin):
    inlines = [InlineMetaTags]


admin.site.register(Category, SimpleCategoryAdmin)
admin.site.register(ContentEntry, ContentEntryAdmin)
admin.site.register(LocalityDomain, LocalityDomainAdmin)
admin.site.register(SiteMeta, SiteMetaAdmin)