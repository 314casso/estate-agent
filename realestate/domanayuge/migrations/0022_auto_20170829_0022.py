# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domanayuge', '0021_sitemeta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitemeta',
            name='site',
            field=models.OneToOneField(to='sites.Site'),
        ),
    ]
