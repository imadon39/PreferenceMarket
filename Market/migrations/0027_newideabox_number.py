# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0026_auto_20160114_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='newideabox',
            name='number',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
