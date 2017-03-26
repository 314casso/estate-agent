# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def gen_key(apps, schema_editor):
    MyModel = apps.get_model('domanayuge', 'Category')
    for row in MyModel.objects.all():
        row.key = row.slug
        row.save()

class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0014_category_key'),
    ]

    operations = [
        migrations.RunPython(gen_key, reverse_code=migrations.RunPython.noop),        
    ]
