from django.db import models
from estatebase.models import Origin
from maxim_base.models import Source

class SourceOrigin(models.Model):
    origin = models.ForeignKey(Origin)
    source_id = models.IntegerField(primary_key=True)
    @property
    def source(self):        
        return Source.objects.get(pk=self.source_id)
    def __unicode__(self):
        return u'%s, %s'  % (self.origin, self.source)
