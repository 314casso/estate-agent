# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from estatebase.models import Locality, Region, EstateType
from django.db.models.signals import m2m_changed
from django.dispatch.dispatcher import receiver
from django.db.utils import IntegrityError

class WordpressMetaAbstract(models.Model):
    name = models.CharField('Name', max_length=150)
    wp_id = models.CharField('Meta Key', max_length=10, blank=True, unique=True)
    def __unicode__(self):
        return self.name
    def get_next_wp_id(self):
        result = self._default_manager.exclude(wp_id='').values_list('wp_id', flat=True)
        result = [int(x.strip()) for x in result]
        return max(result) + 1
    class Meta:        
        abstract = True
        ordering = ['name']
    def save(self, *args, **kwargs):
        self.wp_id = self.get_next_wp_id()
        super(WordpressMetaAbstract, self).save(*args, **kwargs) # Call the "real" save() method.

class WordpressMeta(WordpressMetaAbstract):    
    class Meta:
        verbose_name = u'Населенный пункт'
        verbose_name_plural = u'Населенные пункты'
        
class WordpressMetaEstateType(WordpressMetaAbstract): 
    estate_types = models.ManyToManyField(EstateType, verbose_name=_('EstateType'), blank=True, null=True, related_name='wp_taxons')   
    class Meta:
        verbose_name = u'Вид недвижимости'
        verbose_name_plural = u'Виды недвижимости'        
    
class WordpressTaxonomyTree(MPTTModel):
    name = models.CharField('Name', max_length=150)
    wp_id = models.CharField('WP Id', max_length=10, unique=True)  
    wp_parent_id = models.CharField('WP parent Id', max_length=10, null=True, blank=True,) 
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    up_to_date = models.BooleanField()
    regions = models.ManyToManyField(Region, verbose_name=_('Region'), blank=True, null=True, related_name='wp_taxons')    
    localities = models.ManyToManyField(Locality, verbose_name=_('Locality'), blank=True, null=True, related_name='wp_taxons')    
    wp_meta_locality = models.ForeignKey('WordpressMeta', verbose_name = u'Жесткое поле', blank=True, null=True, related_name='wp_taxon')       
    def __unicode__(self):
        return u'%s' % (self.name,)
    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:        
        verbose_name = u'Рубрика'
        verbose_name_plural = u'Рубрики'    

def load_data(data, model):       
    list_r = data.split(',')
    for item in list_r:
        key,value = item.split(':')
        model.objects.create(wp_id=key.strip(), name=value.strip())

def check_localities():
    ar = [x.lower() for x in WordpressTaxonomyTree.objects.values_list('name',flat=True)]
    #ar = [x.lower() for x in WordpressMeta.objects.filter(wordpress_meta_type=WordpressMeta.LOCALITY).values_list('name',flat=True)]
    #locs = Locality.objects.values_list('name',flat=True)
    locs = WordpressMeta.objects.filter(wordpress_meta_type=WordpressMeta.LOCALITY).values_list('name',flat=True)
    import difflib     
    print '+++++++++++++++++++++++++++++++++++++++++++++++++++++'
    for l in locs:         
        d = difflib.get_close_matches(l.lower(), ar)
        if d:            
            print '%s=%s' % (l,d[0])
            pass
        else:
            print '%s=%s' % (l,'*' * 20)

@receiver(m2m_changed, sender=WordpressTaxonomyTree.localities.through)
def unique_locality(sender, instance, **kwargs):    
    action = kwargs.get('action', None)
    localities = kwargs.get('pk_set', None)
    if action == 'pre_add':
        for locality in localities:
            same_taxonomy = list(WordpressTaxonomyTree.objects.filter(localities=locality))
            if same_taxonomy:                
                raise IntegrityError(u'Населенный пункт c кодом [%s] уже привязан к рубрике "%s" с кодом [%s]' % (locality, same_taxonomy[0].name, same_taxonomy[0].id))
            
# @receiver(pre_save, sender=WordpressMeta)
# def sync_wp_taxonomy(sender, instance, **kwargs):
#     instance.wp_id = WordpressMeta.objects.filter(wordpress_meta_type=WordpressMeta.LOCALITY).aggregate(Max('wp_id'))
         
#check_localities()

#reg = u"2:Ветхий дом, 13:Гараж, 9:Дача, 10:Дачный участок, 1:Дом, 6:Квартира, 12:Коммерческое, 16:Комната, 3:Коттедж, 15:Малосемейка, 14:Новостройки, 4:Полдома, 7:Таунхаус, 8:Участок, 11:Участок сельхозназначения, 5:Часть дома"
#load_data(reg, WordpressMetaEstateType)