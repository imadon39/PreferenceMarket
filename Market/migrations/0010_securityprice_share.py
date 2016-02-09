# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Market.models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0009_auto_20160110_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='securityprice',
            name='share',
            field=Market.models.ListField(default=[], blank=True),
        ),
    ]
