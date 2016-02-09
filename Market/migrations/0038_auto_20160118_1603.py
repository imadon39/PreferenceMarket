# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0037_auto_20160116_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breakdown',
            name='mean_sale_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='breakdown',
            name='sale_rate',
            field=models.FloatField(default=0),
        ),
    ]
