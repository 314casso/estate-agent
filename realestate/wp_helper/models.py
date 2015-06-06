# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from estatebase.models import Locality, Region, EstateType, EstateStatus, Estate,\
    EstateParam
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
        if not self.wp_id:
            self.wp_id = self.get_next_wp_id()
        super(WordpressMetaAbstract, self).save(*args, **kwargs) # Call the "real" save() method.

class WordpressMeta(WordpressMetaAbstract):    
    class Meta:        
        verbose_name = u'Населенный пункт'
        verbose_name_plural = u'Населенные пункты'
        
class WordpressMetaEstateType(WordpressMetaAbstract): 
    estate_types = models.ManyToManyField(EstateType, verbose_name=_('EstateType'), blank=True, null=True, related_name='wp_taxons')   
    class Meta:
        ordering = ['name']
        verbose_name = u'Вид недвижимости'
        verbose_name_plural = u'Виды недвижимости'        

class WordpressMetaRegion(WordpressMetaAbstract): 
    regions = models.ManyToManyField(Region, verbose_name=_('Region'), blank=True, null=True, related_name='wp_taxons')   
    class Meta:
        ordering = ['name']
        verbose_name = u'Район'
        verbose_name_plural = u'Районы'   
    
class WordpressMetaStatus(WordpressMetaAbstract): 
    estate_statuses = models.ManyToManyField(EstateStatus, verbose_name=_('EstateStatus'), blank=True, null=True, related_name='wp_taxons')   
    class Meta:
        ordering = ['name']
        verbose_name = u'Статус'
        verbose_name_plural = u'Статусы'    

class WordpressMetaEstateParam(models.Model): 
    estate_params = models.ManyToManyField(EstateParam, verbose_name=_('EstateParam'), blank=True, null=True, related_name='wp_taxons') 
    taxonomy_tree = models.ForeignKey('WordpressTaxonomyTree', blank=True, null=True,)
    wp_postmeta_key = models.CharField('Postmeta key', max_length=150, blank=True, null=True,)
    wp_postmeta_value = models.CharField('Postmeta value', max_length=150, blank=True, null=True,)
    class Meta:
        ordering = ['id']
        verbose_name = u'Метки'
        verbose_name_plural = u'Метки'
    
class WordpressTaxonomyTree(MPTTModel):
    name = models.CharField('Name', max_length=150)
    wp_id = models.CharField('WP Id', max_length=10, unique=True)  
    wp_parent_id = models.CharField('WP parent Id', max_length=10, null=True, blank=True,) 
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    up_to_date = models.BooleanField()
    regions = models.ManyToManyField(Region, verbose_name=_('Region'), blank=True, null=True,)    
    localities = models.ManyToManyField(Locality, verbose_name=_('Locality'), blank=True, null=True, related_name='wp_taxons')    
    wp_meta_locality = models.ForeignKey('WordpressMeta', verbose_name = u'Жесткое поле', blank=True, null=True, related_name='wp_taxon')       
    def __unicode__(self):
        return u'%s' % (self.name,)
    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:        
        verbose_name = u'Рубрика'
        verbose_name_plural = u'Рубрики'    

class EstateWordpressMeta(models.Model):
    UPTODATE = 5
    MULTIKEYS = 1
    ERROR = 2
    XMLRPC = 3
    UNKNOWN = 4
    STATUS_ERROR = 6
    OUT = 7
    STATE_CHOICES = (
        (UPTODATE, u'Успешно обновлено'),
        (MULTIKEYS, u'Более одного ключа'),
        (ERROR, u'Ошибка обновления'),
        (XMLRPC, u'В очереди на загрузку'),
        (UNKNOWN, u'Не определено'),
        (STATUS_ERROR, u'Ошибка обновления статуса'),
        (OUT, u'Не выгружен на сайт'),
    )
    estate = models.OneToOneField(Estate, related_name='wp_meta')
    post_id = models.CharField('WP Id', max_length=10, unique=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATE_CHOICES, default=UNKNOWN)
    error_message = models.CharField(u'Ошибка', max_length=255, null=True)
    
    def has_error(self):
        return self.status in (self.STATUS_ERROR, self.ERROR, self.UNKNOWN) and self.error_message
    
    def get_error_message(self):
        value = self.error_message        
        parts = [x.strip() for x in value.strip('><').split(":")]
        result = []
        for item in parts:
            try: 
                result.append(eval(item))
            except:
                result.append(item)
        return u': '.join(result)
                

        
            
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

#reg = u"1:Анапский, 3:Новороссийский, 4:Геленджикский, 2:Темрюкский"
#load_data(reg, WordpressMetaRegion)