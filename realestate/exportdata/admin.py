from django.contrib import admin
from exportdata.models import FeedLocality, FeedMapper, BaseFeed, FeedContentType 

admin.site.register(FeedLocality)
admin.site.register(FeedMapper)
admin.site.register(BaseFeed)
admin.site.register(FeedContentType)
