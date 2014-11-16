from django.db import models
from estatebase.models import Locality

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
