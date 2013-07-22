# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from estatebase.models import Locality, Region
from django.db.models.signals import pre_save, post_save, m2m_changed
from wp_helper.service import WPService
from django.dispatch.dispatcher import receiver
from django.db.utils import IntegrityError
from django.db.models.aggregates import Max
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class WordpressMeta(models.Model):    
    LOCALITY = 1
    OBJECT_TYPE = 2    
    METATYPE_CHOICES = (
        (LOCALITY, u'Населенные пункты'),
        (OBJECT_TYPE, u'Тип объекта'),        
    )
    name = models.CharField('Name', max_length=150)
    wp_id = models.CharField('Meta Key', max_length=10, blank=True)
    wordpress_meta_type = models.IntegerField(u'Тип поля', choices=METATYPE_CHOICES)    
    def __unicode__(self):
        return self.name
    class Meta:
        unique_together = ('wp_id', 'wordpress_meta_type')
        ordering = ['name']
        verbose_name = u'Жесткое поле'
        verbose_name_plural = u'Жесткие поля'
    
class WordpressTaxonomyTree(MPTTModel):
    name = models.CharField('Name', max_length=150)
    wp_id = models.CharField('WP Id', max_length=10, unique=True)  
    wp_parent_id = models.CharField('WP parent Id', max_length=10, null=True, blank=True,) 
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    up_to_date = models.BooleanField()
    regions = models.ManyToManyField(Region, verbose_name=_('Region'), blank=True, null=True, related_name='wp_taxons')    
    localities = models.ManyToManyField(Locality, verbose_name=_('Locality'), blank=True, null=True, related_name='wp_taxons')    
    wp_meta_locality = models.ForeignKey('WordpressMeta', verbose_name = u'Жесткое поле', limit_choices_to = {'wordpress_meta_type': WordpressMeta.LOCALITY}, blank=True, null=True, related_name='wp_taxon')       
    def __unicode__(self):
        return u'%s' % (self.name,)
    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:        
        verbose_name = u'Рубрика'
        verbose_name_plural = u'Рубрики'    

def load_data(data, wordpress_meta_type):   
    list_r = data.split(',')
    for item in list_r:
        key,value = item.split(':')
        WordpressMeta.objects.create(wp_id=key.strip(), name=value.strip(), wordpress_meta_type=wordpress_meta_type)

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
#load_data(reg, 2)