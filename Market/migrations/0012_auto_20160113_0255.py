# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0011_auto_20160110_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='breakdown',
            name='initial_investment',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='breakdown',
            name='sale',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='breakdown',
            name='total',
            field=models.FloatField(),
        ),
    ]
