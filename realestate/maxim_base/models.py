from django.db import models

class Source(models.Model):
    name = models.CharField('Name', max_length=50)    
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        db_table = u'source'
        managed = False
    
class Customers(models.Model):
    creator_id = models.IntegerField()
    source = models.ForeignKey(Source)
    treatment_date = models.DateTimeField()
    name = models.CharField(max_length=90)
    comments = models.CharField(max_length=765, blank=True)
    from_where = models.CharField(max_length=765, blank=True)
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        db_table = u'customers'
        managed = False
        
class Contacts(models.Model):
    customer = models.ForeignKey(Customers, related_name='contacts')
    contact = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=36, blank=True)
    update_record = models.DateTimeField()
    def __unicode__(self):
        return u'%s' % self.contact
    class Meta:
        db_table = u'contacts'
        managed = False

class Users(models.Model):
    user = models.CharField(max_length=48)
    name = models.CharField(max_length=75)
    last_logon = models.DateTimeField(null=True, blank=True)
    def __unicode__(self):
        return u'%s (%s)' % (self.name,self.user)
    class Meta:
        db_table = u'users'
        managed = False                