# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Additionals(models.Model):
    id = models.IntegerField(primary_key=True)
    real_estate = models.ForeignKey(RealEstate, unique=True)
    name = models.CharField(max_length=150, unique=True)
    value = models.CharField(max_length=300)
    class Meta:
        db_table = u'additionals'

class Area(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300, unique=True)
    class Meta:
        db_table = u'area'

class Contacts(models.Model):
    id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customers)
    contact = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=36, blank=True)
    update_record = models.DateTimeField()
    class Meta:
        db_table = u'contacts'

class CustomerHasRealEstate(models.Model):
    real_estate = models.ForeignKey(RealEstate, unique=True)
    customer = models.ForeignKey(Customers)
    class Meta:
        db_table = u'customer_has_real_estate'

class CustomerWork(models.Model):
    id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customers)
    user_id = models.IntegerField()
    stage = models.CharField(max_length=75)
    description = models.CharField(max_length=765, blank=True)
    creation_date = models.DateTimeField()
    class Meta:
        db_table = u'customer_work'


#+++
class Customers(models.Model):
    id = models.IntegerField(primary_key=True)
    creator_id = models.IntegerField()
    source_id = models.IntegerField()
    treatment_date = models.DateTimeField()
    name = models.CharField(max_length=90)
    comments = models.CharField(max_length=765, blank=True)
    from_where = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'customers'

class Descriptions(models.Model):
    id = models.IntegerField(primary_key=True)
    real_estate = models.ForeignKey(RealEstate, unique=True)
    description = models.TextField()
    class Meta:
        db_table = u'descriptions'

class Floors(models.Model):
    id = models.IntegerField(primary_key=True)
    real_estate = models.ForeignKey(RealEstate)
    name = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'floors'

class Images(models.Model):
    id = models.IntegerField(primary_key=True)
    real_estate = models.ForeignKey(RealEstate)
    file_name = models.CharField(max_length=96)
    class Meta:
        db_table = u'images'

class OrderHasPlace(models.Model):
    order = models.ForeignKey(Orders)
    place = models.ForeignKey(Place)
    class Meta:
        db_table = u'order_has_place'

class OrderHasRegion(models.Model):
    order = models.ForeignKey(Orders)
    region = models.ForeignKey(Region)
    class Meta:
        db_table = u'order_has_region'

class OrderHasType(models.Model):
    order = models.ForeignKey(Orders)
    type = models.ForeignKey(Types)
    class Meta:
        db_table = u'order_has_type'

class OrderHasUser(models.Model):
    order = models.ForeignKey(Orders)
    user = models.ForeignKey(Users)
    class Meta:
        db_table = u'order_has_user'

class OrderProperties(models.Model):
    id = models.IntegerField(primary_key=True)
    order = models.ForeignKey(Orders)
    name = models.CharField(max_length=90, unique=True)
    value = models.CharField(max_length=765)
    class Meta:
        db_table = u'order_properties'

class Orders(models.Model):
    id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customers)
    creator_id = models.IntegerField()
    creation_date = models.DateTimeField()
    last_editor_id = models.IntegerField(null=True, blank=True)
    update_record = models.DateTimeField()
    status = models.CharField(max_length=60)
    cost_from = models.IntegerField(null=True, blank=True)
    cost_to = models.IntegerField(null=True, blank=True)
    operation = models.TextField(blank=True)
    result = models.TextField(blank=True)
    class Meta:
        db_table = u'orders'

class Place(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=75, unique=True)
    class Meta:
        db_table = u'place'

class Properties(models.Model):
    id = models.IntegerField(primary_key=True)
    real_estate = models.ForeignKey(RealEstate, unique=True)
    name = models.CharField(max_length=75, unique=True)
    value = models.CharField(max_length=765)
    class Meta:
        db_table = u'properties'

class RealEstate(models.Model):
    id = models.IntegerField(primary_key=True)
    type_id = models.IntegerField()
    creator_id = models.IntegerField()
    source_id = models.IntegerField()
    creation_date = models.DateTimeField()
    last_editor_id = models.IntegerField(null=True, blank=True)
    update_record = models.DateTimeField()
    region_id = models.IntegerField()
    place_id = models.IntegerField(null=True, blank=True)
    street_id = models.IntegerField(null=True, blank=True)
    house_number = models.CharField(max_length=15, blank=True)
    area_id = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    cost_markup = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=42)
    class Meta:
        db_table = u'real_estate'

class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=90, unique=True)
    class Meta:
        db_table = u'region'

class Rooms(models.Model):
    id = models.IntegerField(primary_key=True)
    floor = models.ForeignKey(Floors)
    name = models.CharField(max_length=75)
    area = models.FloatField(null=True, blank=True)
    furniture = models.CharField(max_length=30, blank=True)
    feature = models.CharField(max_length=45, blank=True)
    additional = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = u'rooms'

class Selection(models.Model):
    id = models.IntegerField(primary_key=True)
    order = models.ForeignKey(Orders)
    creator = models.ForeignKey(Users, null=True, blank=True)
    creation_date = models.DateTimeField()
    comments = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'selection'

class SelectionItems(models.Model):
    selection = models.ForeignKey(Selection)
    real_estate = models.ForeignKey(RealEstate)
    class Meta:
        db_table = u'selection_items'

class Source(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    class Meta:
        db_table = u'source'

class Street(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=75, unique=True)
    class Meta:
        db_table = u'street'

class Types(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=90, unique=True)
    list_item = models.CharField(max_length=45)
    mask = models.CharField(max_length=135)
    class Meta:
        db_table = u'types'

class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=48)
    password = models.CharField(max_length=126)
    name = models.CharField(max_length=75)
    last_logon = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'users'

