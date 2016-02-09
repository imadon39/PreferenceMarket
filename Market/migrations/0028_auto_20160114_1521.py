# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0027_newideabox_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='newideabox',
            name='contain_newAdd',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='newideabox',
            name='newAdd',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='newideabox',
            name='newLevel',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
