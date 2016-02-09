# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0036_playerresult_product_sales'),
    ]

    operations = [
        migrations.AddField(
            model_name='breakdown',
            name='mean_sale_rate',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='breakdown',
            name='sale_rate',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='designer',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
