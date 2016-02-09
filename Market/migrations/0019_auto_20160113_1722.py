# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0018_lmsr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='market',
            name='player_number',
        ),
        migrations.AddField(
            model_name='product',
            name='player_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
