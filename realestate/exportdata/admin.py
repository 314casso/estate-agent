from django.contrib import admin
from exportdata.models import FeedLocality, BaseFeed, ContentTypeMapper, FeedEngine, ValueMapper, MappedNode, MarketingCampaign
 

admin.site.register(FeedLocality)
admin.site.register(BaseFeed)
admin.site.register(ContentTypeMapper)
admin.site.register(FeedEngine)
admin.site.register(ValueMapper)
admin.site.register(MappedNode)
admin.site.register(MarketingCampaign)