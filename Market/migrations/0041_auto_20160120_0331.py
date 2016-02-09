# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Market.models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0040_designer_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='order',
            field=Market.models.ListField(default=[], blank=True),
        ),
    ]
