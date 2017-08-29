# -*- coding: utf-8 -*-
from django.utils.encoding import force_text, force_unicode
from django.db import models
from categories.base import CategoryBase
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from orderedmodel.models import OrderedModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,\
    GenericRelation
import os
from estatebase.models import Locality
from django.core.urlresolvers import reverse
from django.contrib.postgres.fields import ArrayField
from django.contrib.sites.models import Site


def get_file_upload_to(instance, filename): 
    if hasattr(instance, 'content_type'):   
        return os.path.join('files', force_unicode(instance.content_type.id), force_unicode(instance.object_id),  force_unicode(filename))
    return os.path.join('images', force_unicode(instance.id), force_unicode(filename))


@python_2_unicode_compatible
class Category(CategoryBase):
    alternate_title = models.CharField(blank=True, default="", max_length=200)  
    description = models.TextField(blank=True, null=True)
    alternate_url = models.CharField(blank=True, max_length=200,)
    order = models.IntegerField(default=0)
    menu = models.BooleanField(default=True)
    key = models.CharField(max_length=50, unique=True, db_index=True)
    image = models.ImageField(verbose_name=_('Image'), upload_to=get_file_upload_to, blank=True, null=True,) 
    
    def active_entries(self):
        return self.entries.filter(active=True)
           
    def __str__(self):
        ancestors = self.get_ancestors()
        return ' > '.join([force_text(i.name) for i in ancestors] + [self.name, ])
    
    class Meta(CategoryBase.Meta):        
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        order_insertion_by = ('order', 'name')
    
    
@python_2_unicode_compatible    
class ContentEntry(models.Model):     
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(verbose_name=_('slug'))
    active = models.BooleanField(default=True, verbose_name=_('active'))    
    publication_date = models.DateTimeField(
        _('publication date'),
        db_index=True, default=timezone.now,
        help_text=_("Used to build the entry's URL."))
    summary = models.TextField(_('summary'), blank=True, null=True)
    content = models.TextField(_('content'), blank=True)
    categories = models.ManyToManyField(Category, related_name='entries')
        
    links = GenericRelation('MediaLink')
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)    
    
    def __str__(self):        
        return force_text(self.title)
    
    def get_absolute_url(self):        
        return reverse('page', args=[self.slug])
                
    def baseimage(self):        
        return self.images().first()
    
    def social_links(self):
        return self.links.filter(linktype=MediaLink.SOCIAL)    
    
    def free_links(self):
        return self.links.filter(linktype=MediaLink.FREE)
    
    def images(self):
        return self.links.filter(linktype=MediaLink.IMAGE)
    
    class Meta:
        ordering = ['-publication_date']
        get_latest_by = 'publication_date'
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        index_together = [['slug', 'publication_date']]


@python_2_unicode_compatible        
class MediaLink(OrderedModel):
    FREE = 1
    IMAGE = 2    
    CONTACT = 3    
    MESSENGER = 4
    SOCIAL = 5    
    TYPE_CHOICES = (
        (FREE, u'Ссылка'),
        (IMAGE, u'Картинка'),        
        (CONTACT, u'Контакт'),
        (MESSENGER, u'Мессенджер'),
        (SOCIAL, u'Соцсеть'),
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    title = models.CharField(_('title'), max_length=255)
    url = models.URLField(_('url'), max_length=100, blank=True, null=True,)
    icon_class = models.CharField(_('Icon class'), max_length=50, blank=True, null=True,)
    image = models.ImageField(verbose_name=_('Image'), upload_to=get_file_upload_to, blank=True, null=True,)
    linktype = models.PositiveIntegerField(verbose_name=_('LinkType'), choices=TYPE_CHOICES, default=IMAGE)
        
    def __str__(self):
        return force_unicode(self.title)
    class Meta(OrderedModel.Meta):
        verbose_name = _('MediaLink')
        verbose_name_plural = _('MediaLinks')  
        
        
@python_2_unicode_compatible        
class LocalityDomain(models.Model):
    locality = models.ForeignKey(Locality)
    domain = models.CharField(blank=True, max_length=150, db_index=True, )
    active = models.BooleanField(default=True, verbose_name=_('active'))
    in_title = models.BooleanField(default=False, verbose_name=_('in_title')) 
    def __str__(self):        
        return '%s %s' % (force_text(self.locality), force_text(self.domain))    
    
    
@python_2_unicode_compatible        
class SiteMeta(models.Model):
    site = models.OneToOneField(Site)
    main_mirror = models.CharField(blank=True, null=True, max_length=150)
    title = models.CharField(blank=True, null=True, max_length=250)      
    description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    def __str__(self):        
        return '%s' % (force_text(self.site))    


class MetaTag (models.Model):   
    site_meta = models.ForeignKey(SiteMeta)
    name = models.CharField(blank=True, null=True, max_length=150)
    content = models.CharField(blank=True, null=True, max_length=250)    
    