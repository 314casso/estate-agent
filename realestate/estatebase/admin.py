from django.contrib import admin
from models import Region, Locality, Microdistrict, Street, Estate, EstateType, EstateTypeCategory
from django.contrib.contenttypes.models import ContentType
from orderedmodel.admin import OrderedModelAdmin
from estatebase.models import ClientType, Client, ContactType, Origin, Contact,\
    ContactState, ContactHistory, Bidg, EstateStatus, Document, EstateParam,\
    Beside, Electricity, Watersupply, Gassupply, Sewerage, Telephony, Internet,\
    Driveway, LevelName, EstatePhoto, Stead, UserProfile, GeoGroup, Bid,\
    ComStatus, Office, Appliance, BidEventCategory, RegisterCategory,\
    WallConstrucion, ExteriorFinish, Interior
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from maxim_base.models import Source , Customers, Contacts


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

class EstateParamAdmin(OrderedModelAdmin):
    list_display = ['name', 'reorder']


admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]

admin.site.register(User, UserProfileAdmin)

admin.site.register(Region)
admin.site.register(Locality)
admin.site.register(Microdistrict)
admin.site.register(Street, StreetAdmin)
admin.site.register(ContentType)
admin.site.register(Estate)
admin.site.register(EstateType,EstateTypeAdmin)
admin.site.register(EstateTypeCategory,EstateTypeCategoryAdmin)

admin.site.register(ClientType)
admin.site.register(Client)
admin.site.register(ContactType)
admin.site.register(Origin)
admin.site.register(Contact)
admin.site.register(ContactState)
admin.site.register(ContactHistory)
admin.site.register(Bidg)
admin.site.register(EstateStatus)
admin.site.register(Document)
admin.site.register(EstateParam,EstateParamAdmin)
admin.site.register(Beside)
admin.site.register(Electricity)                    
admin.site.register(Watersupply)
admin.site.register(Gassupply)
admin.site.register(Sewerage)
admin.site.register(Telephony)
admin.site.register(Internet)
admin.site.register(Driveway)
admin.site.register(LevelName)
admin.site.register(EstatePhoto)
admin.site.register(Stead)
admin.site.register(UserProfile)
admin.site.register(GeoGroup)
admin.site.register(Bid)
admin.site.register(ComStatus)
admin.site.register(Office)
admin.site.register(Appliance)
admin.site.register(BidEventCategory)
admin.site.register(RegisterCategory)
admin.site.register(WallConstrucion)
admin.site.register(ExteriorFinish)
admin.site.register(Interior)
