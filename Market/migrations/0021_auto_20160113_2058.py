# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0020_auto_20160113_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interaction',
            name='level1',
        ),
        migrations.RemoveField(
            model_name='interaction',
            name='level2',
        ),
        migrations.RemoveField(
            model_name='level',
            name='interaction',
        ),
        migrations.DeleteModel(
            name='Interaction',
        ),
    ]
