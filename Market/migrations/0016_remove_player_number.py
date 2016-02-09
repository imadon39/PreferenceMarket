# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0015_market_player_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='number',
        ),
    ]
