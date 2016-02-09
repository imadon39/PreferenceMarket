# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0029_auto_20160114_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='newideabox',
            name='newAdd_name',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='newideabox',
            name='newLevel_name',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
