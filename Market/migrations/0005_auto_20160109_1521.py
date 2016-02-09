# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0004_auto_20160105_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricehistory',
            name='market',
        ),
        migrations.RemoveField(
            model_name='securityresult',
            name='product',
        ),
        migrations.DeleteModel(
            name='PriceHistory',
        ),
        migrations.DeleteModel(
            name='SecurityResult',
        ),
    ]
