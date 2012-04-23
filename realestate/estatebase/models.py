# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Estate(models.Model):
    pass

class SimpleDict(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        ordering = ('name',)
        abstract = True

class Region(SimpleDict):
    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')

class Locality(SimpleDict):
    region = models.ForeignKey(Region,blank=True,null=True,verbose_name=_('Region'),)
    class Meta:
        verbose_name = _('locality')
        verbose_name_plural = _('localities')    

class Microdistrict(SimpleDict):
    locality = models.ForeignKey(Locality,verbose_name=_('Locality'),)
    class Meta:
        verbose_name = _('microdistrict')
        verbose_name_plural = _('microdistricts')

class Street(SimpleDict):
    locality = models.ForeignKey(Locality,verbose_name=_('Locality'),)
    class Meta:
        verbose_name = _('street')
        verbose_name_plural = _('streets')
        