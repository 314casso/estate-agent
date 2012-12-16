from django.contrib import admin
from maxim_base.models import Source, Customers, Contacts, Users, RealEstate,\
    Types, Images

admin.site.register(Source)
admin.site.register(Customers)
admin.site.register(Contacts)    
admin.site.register(Users)
admin.site.register(RealEstate)
admin.site.register(Types)
admin.site.register(Images)