from django.db import models
from estatebase.models import Locality
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

class FeedLocality(models.Model):    
    feed_name = models.CharField(db_index=True, max_length=15)
    locality = models.ForeignKey(Locality, on_delete=models.PROTECT)
    feed_code = models.CharField(db_index=True, max_length=15)
    def __unicode__(self):
        return u'%s' % self.locality
    class Meta:
        ordering = ['locality']
        unique_together = ('feed_name', 'locality')    
        unique_together = ('feed_code', 'locality')

class FeedMapper(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    feed_name = models.CharField(db_index=True, max_length=15)  
    xml_value = models.CharField(db_index=True, max_length=255)