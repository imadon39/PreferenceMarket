# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Market.models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0041_auto_20160120_0331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='breakdown',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='breakdown',
            name='gross_margin',
        ),
        migrations.RemoveField(
            model_name='security',
            name='add_cost',
        ),
        migrations.AddField(
            model_name='player',
            name='email',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='is_answered',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='playerresult',
            name='returned',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='newideabox',
            name='newAttribute',
            field=Market.models.ListField(default=[], blank=True),
        ),
        migrations.AlterField(
            model_name='newideabox',
            name='newAttribute_name',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='newideabox',
            name='newLevel',
            field=Market.models.ListField(default=[], blank=True),
        ),
        migrations.AlterField(
            model_name='newideabox',
            name='newLevel_name',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pricehistory',
            name='data',
            field=Market.models.ListField(default=[], blank=True),
        ),
    ]
