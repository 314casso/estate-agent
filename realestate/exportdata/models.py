from django.db import models
from estatebase.models import Locality, EstateTypeCategory, EstateParam, Estate,\
    EstateType
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import datetime
from django.db.models.query_utils import Q
from django.utils.translation import ugettext_lazy as _
      

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
    YANDEX = 'YANDEX'
    WP = 'WORDPRESS'
    FEEDENGINE_CHOICES = (
        (AVITO, 'Avito'),        
        (YANDEX, 'Yandex'),
        (WP, 'Wordpress'),
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
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
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
    MIN_PRICE_LIMIT = 100000
    name = models.CharField(verbose_name=_('Name'), db_index=True, max_length=15)
    active = models.BooleanField(verbose_name=_('Active'), )    
    estate_categories = models.ManyToManyField(EstateTypeCategory, verbose_name=_('EstateTypeCategory'),)
    estate_types = models.ManyToManyField(EstateType, verbose_name=_('EstateType'), blank=True)
    estate_param = models.ForeignKey(EstateParam, verbose_name=_('EstateParam'), blank=True, null=True,)
    valid_days = models.IntegerField(verbose_name=_('ValidDays'), )
    feed_engine = models.ForeignKey(FeedEngine, verbose_name=_('FeedEngine'), )        
    campaign = models.ForeignKey(MarketingCampaign, verbose_name=_('Campaign'), blank=True, null=True,)    
    note = models.CharField(verbose_name=_('Note'), max_length=255, blank=True, null=True,)        
    use_broker = models.BooleanField(verbose_name=_('UseBroker'), default=False)
    use_possible_street = models.BooleanField(verbose_name=_('UsePossibleStreet'), default=False)
    show_bld_number = models.BooleanField(verbose_name=_('ShowBldNumber'), default=False)
    only_valid = models.BooleanField(verbose_name=_('OnlyValid'), default=True)    
    min_price_limit = models.IntegerField(verbose_name=_('MinPriceLimit'), default=MIN_PRICE_LIMIT, blank=True, null=True,)
              
    def __unicode__(self):
        return u'%s' % self.name        
    
    def get_delta(self):    
        if self.valid_days:
            return datetime.datetime.now() - datetime.timedelta(days=self.valid_days)
    
    def get_queryset(self):
        f = {}
        q = Estate.objects.all()
        
        if self.estate_param:
            f['estate_params__exact'] = self.estate_param
        
        if self.min_price_limit:
            f['agency_price__gte'] = self.min_price_limit
        
        if self.only_valid:
            f['validity'] = Estate.VALID
            
               
        type_fifter = Q()        
        cats = list(self.estate_categories.all())       
        types = list(self.estate_types.all())        
        for t in types:
            if t.estate_type_category in cats:
                cats.remove(t.estate_type_category)
            type_fifter = type_fifter | Q(bidgs__estate_type_id__exact=t.pk, estate_category_id__exact=t.estate_type_category_id)
            type_fifter = type_fifter | Q(stead__estate_type_id__exact=t.pk, estate_category_id__exact=t.estate_type_category_id)
        if len(cats):
            type_fifter = type_fifter | Q(estate_category__in=cats)
        
        f['Q'] = type_fifter
                
        delta = self.get_delta()
        if delta:
            f['history__modificated__gte'] = delta             
        
        return self.set_filter(q, f)       
    
    def set_filter(self, q, filter_dict):
        if 'Q' in filter_dict:
            q = q.filter(filter_dict.pop('Q'))          
        if len(filter_dict):
            q = q.filter(**filter_dict)            
        return q.distinct()
    
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
    