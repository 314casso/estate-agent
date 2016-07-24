from django.db import models
from estatebase.models import Locality, EstateTypeCategory, EstateParam, Estate
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
import datetime
      

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


class FeedEngine(models.Model):
    AVITO = 'AVITO'     
    FEEDENGINE_CHOICES = (
        (AVITO, 'Avito'),        
    )          
    name = models.CharField(db_index=True, max_length=15)
    engine = models.CharField(
        max_length=15,
        choices=FEEDENGINE_CHOICES,
        default=AVITO,
    )    
    def __unicode__(self):        
        return u'%s' % self.name
    
    def get_engine(self):
        return


class MappedNode(models.Model):
    xml_node = models.CharField(db_index=True, max_length=50)
    type_mapper = models.ForeignKey('ContentTypeMapper', related_name='nodes')
    def __unicode__(self):
        return u'%s: %s' % (self.xml_node, self.type_mapper)


class MarketingCampaign(models.Model):
    name = models.CharField(db_index=True, max_length=15)
    start_date = models.DateTimeField(default=datetime.datetime.now())
    end_date = models.DateTimeField(blank=True, null=True,)
    phone = models.CharField(max_length=50, blank=True, null=True,)
    email = models.EmailField(blank=True, null=True,)
    person = models.CharField(max_length=255, blank=True, null=True,)
    active = models.BooleanField()
    note = models.CharField(max_length=255, blank=True, null=True,)
    
    @property
    def valid(self):
        start_date = self.start_date
        end_date = self.end_date if self.end_date else datetime.datetime.strptime('31123000', "%d%m%Y")
        return self.active and (start_date <= datetime.datetime.now() <= end_date)
                   
    def __unicode__(self):
        return u'%s' % self.name
    

class BaseFeed(models.Model):
    name = models.CharField(db_index=True, max_length=15)
    active = models.BooleanField()    
    estate_categories = models.ManyToManyField(EstateTypeCategory)
    estate_param = models.ForeignKey(EstateParam, blank=True, null=True,)
    valid_days = models.IntegerField()
    feed_engine = models.ForeignKey(FeedEngine, )        
    campaign = models.ForeignKey(MarketingCampaign, blank=True, null=True,)    
    note = models.CharField(max_length=255, blank=True, null=True,)        
    
          
    def __unicode__(self):
        return u'%s' % self.name        
    
    def get_delta(self):    
        if self.valid_days:
            return datetime.datetime.now() - datetime.timedelta(days=self.valid_days)
    
    def get_queryset(self):
        MIN_PRICE_LIMIT = 100000  
        f = {
             'validity':Estate.VALID,      
             'agency_price__gte': MIN_PRICE_LIMIT,
             'estate_category_id__in': (list(self.estate_categories.all())),             
             'estate_params__exact': self.estate_param,             
             }
        
        delta = self.get_delta()
        if delta:
            f['history__modificated__gte'] = delta
            
        q = Estate.objects.all()
        q = q.filter(**f)
        return q
    
    def get_feed_engine(self):
        return self.feed_engine.get_engine()(self)
        

class ValueMapper(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    mapped_node = models.ForeignKey(MappedNode)  
    xml_value = models.CharField(db_index=True, max_length=255, blank=True, null=True,)
    class Meta:
        unique_together = ('content_type', 'object_id', 'mapped_node')

    
class ContentTypeMapper(models.Model):
    feed_engine = models.ForeignKey(FeedEngine)    
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    filter = models.CharField(max_length=255, blank=True, null=True,)
    order_by = models.CharField(max_length=150, blank=True, null=True,)
    def __unicode__(self):
        return u'%s (%s)' % (self.content_type, self.feed_engine)
    class Meta:
        unique_together = ('feed_engine', 'content_type')
    