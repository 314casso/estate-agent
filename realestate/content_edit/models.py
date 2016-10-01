from django.db import models

try:
    from django.contrib.sites.models import Site
    from django.contrib.sites.managers import CurrentSiteManager
    site = True
except ImportError:
    site = None

class CmsContent(models.Model):
    """ CMS like Content area """
    name = models.CharField(max_length=255, unique=True)
    content = models.TextField(blank=True)
    objects = models.Manager()
    if site:
        on_site = CurrentSiteManager()
        site = models.ForeignKey(Site)

    def __unicode__(self):
        return self.name
