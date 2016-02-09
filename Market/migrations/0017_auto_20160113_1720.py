# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0016_remove_player_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lmsr',
            name='market',
        ),
        migrations.DeleteModel(
            name='LMSR',
        ),
    ]
