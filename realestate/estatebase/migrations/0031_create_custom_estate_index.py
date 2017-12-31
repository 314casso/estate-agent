# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatebase', '0030_auto_20171231_0133'),
    ]

    operations = [
        migrations.RunSQL(          
            "CREATE INDEX index_estate_id ON public.estatebase_estate USING btree (id DESC, agency_price, actualized, estate_category_id);",
            "DROP INDEX index_estate_id;",
        )
    ]
