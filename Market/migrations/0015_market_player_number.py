# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0014_lmsr'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='player_number',
            field=models.IntegerField(default=0),
        ),
    ]
