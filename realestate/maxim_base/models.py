from django.db import models

class Source(models.Model):
    name = models.CharField('Name', max_length=50)
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        db_table = 'source'
        managed = False
    
