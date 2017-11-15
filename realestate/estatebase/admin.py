from django.contrib import admin
from models import Region, Locality, Microdistrict, Street, Estate, EstateType, EstateTypeCategory
from django.contrib.contenttypes.models import ContentType
from orderedmodel.admin import OrderedModelAdmin
from estatebase.models import ClientType, Client, ContactType, Origin, Contact,\
    ContactState, ContactHistory, Bidg, EstateStatus, Document, EstateParam,\
    Beside, Electricity, Watersupply, Gassupply, Sewerage, Telephony, Internet,\
    Driveway, LevelName, EstatePhoto, Stead, UserProfile, GeoGroup, Bid,\
    ComStatus, Office, Appliance, BidEventCategory, RegisterCategory,\
    WallConstrucion, ExteriorFinish, Interior, WallFinish, EstateClientStatus,\
    BidEvent, BidStatus, LayoutFeature, Furniture, LayoutType,\
    Ceiling, Flooring, Heating, Roof, WindowType, Shape, Purpose, LocalityType,\
    Validity, EstateRegister, StreetType, LandType, YandexBuilding, DealStatus,\
    EstateFile, GenericLink, GenericSupply, Supply, SupplyState, BuildingItem,\
    BidStatusCategory, DocumentType, BidState
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

class StreetAdmin(admin.ModelAdmin):
    list_filter = ('locality',)
    raw_id_admin = ('locality',)
    search_fields = ['name',]

class EstateTypeline(admin.TabularInline):
    model = EstateType

class EstateTypeAdmin(OrderedModelAdmin):
    list_display = ['name', 'name_accs',  'reorder']
    list_filter = ('estate_type_category',)
    raw_id_admin = ('estate_type_category',)

class EstateTypeCategoryAdmin(OrderedModelAdmin):
    list_display = ['name', 'reorder']
    inlines = [
        EstateTypeline,
    ]

class EstateParamAdmin(OrderedModelAdmin):
    list_display = ['name', 'reorder']

class BidgInline(admin.StackedInline):
    model = Bidg    
    extra = 0
    fields = ['estate_type', 'basic']
    
class SteadInline(admin.StackedInline):
    model = Stead    
    extra = 0
    fields = ['estate_type', 'total_area']
    
class EstateAdmin(admin.ModelAdmin):
    search_fields = ['id',]
    fields = ['estate_category', 'deleted']
    inlines = [BidgInline, SteadInline]
    list_filter = ('deleted',)
    def get_queryset(self, request):                
        return Estate.all_objects.all()

class ClientAdmin(admin.ModelAdmin):
    search_fields = ['id',]
    fields = ['name', 'deleted']
    list_display = ('id', '__unicode__')
    list_filter = ('deleted',)
    def get_queryset(self, request):                
        return Client.all_objects.all()    

class ContactAdmin(admin.ModelAdmin):
    raw_id_fields = ('client',)
    search_fields = ['contact',]
    list_filter = ('contact_type',) 

class BidgAdmin(admin.ModelAdmin):
    search_fields = ['estate__id']
    fields = ['estate_type', 'basic']

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline,]

class BidAdmin(admin.ModelAdmin):
    search_fields = ['id',]
    fields = ['deleted']
    list_display = ('id', '__unicode__',)
    list_filter = ('deleted',)
    def queryset(self, request):                
        return Bid.all_objects

class LocalityAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_gent', 'name_loct']
    
class BidEventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_calendar', 'do_free']
    
class RegionAdmin(admin.ModelAdmin):
    list_display = ['regular_name', 'regular_name_gent']    

class FileInline(GenericTabularInline):
    model = EstateFile
    
class LinkInline(GenericTabularInline):
    model = GenericLink    
    
class SupplyInline(GenericTabularInline):
    model = GenericSupply    
    
class ItemInline(admin.TabularInline):
    model = BuildingItem
    
class YandexBuildingAdmin(admin.ModelAdmin):
    inlines = [
        SupplyInline, FileInline, LinkInline, ItemInline
    ]    
    
class MicrodistrictAdmin(admin.ModelAdmin):
    search_fields = ['name',]    
   
class BidStatusAdmin(admin.ModelAdmin):
    list_filter = ('category',)    
    
class BidStateAdmin(admin.ModelAdmin):
    raw_id_fields = ('bid',)    
    list_display = ('bid', 'state')
    
admin.site.register(User, UserProfileAdmin)

admin.site.register(Region, RegionAdmin)
admin.site.register(Locality, LocalityAdmin)
admin.site.register(Microdistrict, MicrodistrictAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(ContentType)
admin.site.register(Estate, EstateAdmin)
admin.site.register(EstateType,EstateTypeAdmin)
admin.site.register(EstateTypeCategory,EstateTypeCategoryAdmin)

admin.site.register(ClientType)
admin.site.register(ContactType)
admin.site.register(Origin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactState)
admin.site.register(ContactHistory)
admin.site.register(Bidg, BidgAdmin)
admin.site.register(EstateStatus)
admin.site.register(Document)
admin.site.register(EstateParam,EstateParamAdmin)
admin.site.register(Beside, LocalityAdmin)
admin.site.register(Electricity)                    
admin.site.register(Watersupply)
admin.site.register(Gassupply)
admin.site.register(Sewerage)
admin.site.register(Telephony)
admin.site.register(Internet)
admin.site.register(Driveway)
admin.site.register(LevelName)
admin.site.register(EstatePhoto)
admin.site.register(LandType)
#admin.site.register(UserProfile)
admin.site.register(GeoGroup)
admin.site.register(Bid, BidAdmin)
admin.site.register(ComStatus)
admin.site.register(Office)
admin.site.register(Appliance)
admin.site.register(BidEventCategory, BidEventCategoryAdmin)
admin.site.register(RegisterCategory)
admin.site.register(WallConstrucion)
admin.site.register(ExteriorFinish)
admin.site.register(Interior)
admin.site.register(WallFinish)
admin.site.register(EstateClientStatus)
admin.site.register(BidEvent)
admin.site.register(BidStatus, BidStatusAdmin)
admin.site.register(LayoutType)
admin.site.register(LayoutFeature)
admin.site.register(Furniture)
admin.site.register(Ceiling)
admin.site.register(Flooring)
admin.site.register(Heating)
admin.site.register(Roof)
admin.site.register(WindowType)
admin.site.register(Client, ClientAdmin)
admin.site.register(Shape)
admin.site.register(Purpose)
admin.site.register(LocalityType)
admin.site.register(StreetType)
admin.site.register(Validity)
admin.site.register(YandexBuilding, YandexBuildingAdmin)
admin.site.register(DealStatus)
admin.site.register(Supply)
admin.site.register(SupplyState)
admin.site.register(BuildingItem)
admin.site.register(BidStatusCategory)
admin.site.register(DocumentType)
admin.site.register(BidState, BidStateAdmin)

