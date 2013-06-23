from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from estatebase.models import EstateType, Locality


class WordpressTaxonomyTree(MPTTModel):
    name = models.CharField('Name', max_length=150)
    wp_id = models.CharField('WP Id', max_length=10)  
    wp_parent_id = models.CharField('WP parent Id', max_length=10, null=True, blank=True,) 
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    up_to_date = models.BooleanField()
    estate_types = models.ManyToManyField(EstateType, verbose_name=_('EstateType'), blank=True, null=True)
    localities = models.ManyToManyField(Locality, verbose_name=_('Locality'), blank=True, null=True)    
    def __unicode__(self):
        return self.name
        #return u'%s [%s] [%s]' % (self.name, ', '.join(self.localities.values_list('name', flat=True)), ', '.join(self.estate_types.values_list('name', flat=True)) )
    class MPTTMeta:
        order_insertion_by = ['name']    
    