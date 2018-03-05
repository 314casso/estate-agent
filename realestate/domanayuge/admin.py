from django.contrib import admin
from domanayuge.models import Category, ContentEntry, MediaLink, LocalityDomain,\
    SiteMeta, MetaTag
from categories.base import CategoryBaseAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.admin.options import TabularInline
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class SimpleCategoryAdmin(CategoryBaseAdmin):
    pass


class InlineLinkEnties(GenericTabularInline):
    model = MediaLink
    extra = 1

class InlineMetaTags(TabularInline):
    model = MetaTag
    extra = 1


class ContentEntryAdmin(admin.ModelAdmin):
    list_filter = ['categories']
    inlines = [InlineLinkEnties]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', 'slug']
    

class LocalityDomainAdmin(admin.ModelAdmin):
    pass

class SiteMetaAdmin(admin.ModelAdmin):
    inlines = [InlineMetaTags,InlineLinkEnties]


admin.site.register(Category, SimpleCategoryAdmin)
admin.site.register(ContentEntry, ContentEntryAdmin)
admin.site.register(LocalityDomain, LocalityDomainAdmin)
admin.site.register(SiteMeta, SiteMetaAdmin)
