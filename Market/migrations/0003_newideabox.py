# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Market.models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0002_auto_20151215_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewIdeaBox',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attributes', Market.models.ListField()),
                ('attribute_name', models.CharField(default=b'', max_length=300)),
                ('add_market', models.BooleanField(default=False)),
                ('player', models.ForeignKey(to='Market.Player')),
                ('product', models.ForeignKey(to='Market.Product')),
            ],
        ),
    ]
