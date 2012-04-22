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
    pass
