# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Market.models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0022_auto_20160113_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='order',
            field=Market.models.ListField(default=[]),
        ),
    ]
