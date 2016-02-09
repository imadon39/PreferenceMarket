# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Market.models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0028_auto_20160114_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newideabox',
            name='newAdd',
            field=Market.models.ListField(null=True),
        ),
        migrations.AlterField(
            model_name='newideabox',
            name='newLevel',
            field=Market.models.ListField(null=True),
        ),
    ]
