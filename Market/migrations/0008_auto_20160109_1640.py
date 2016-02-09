# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0007_auto_20160109_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='securityresult',
            name='histories',
        ),
        migrations.AddField(
            model_name='pricehistory',
            name='histories',
            field=models.ManyToManyField(to='Market.SecurityResult', through='Market.History'),
        ),
    ]
