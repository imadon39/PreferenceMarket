# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Market.models


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0005_auto_20160109_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('data', Market.models.ListField(default=[])),
                ('is_open', models.BooleanField(default=True)),
                ('product', models.ForeignKey(to='Market.Product')),
            ],
        ),
        migrations.CreateModel(
            name='SecurityResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=200)),
                ('attributes', Market.models.ListField(default=[], blank=True)),
                ('attribute_name', models.CharField(default=b'', max_length=300)),
                ('last_price_result', models.FloatField(default=0)),
                ('VWAP_result', models.FloatField(default=0)),
                ('number', models.IntegerField()),
                ('GA_setting', models.BooleanField(default=False)),
                ('estimate_time', models.DateTimeField(verbose_name=b'estimate_time')),
                ('history', models.ForeignKey(to='Market.PriceHistory')),
                ('product', models.ForeignKey(to='Market.Product')),
            ],
        ),
    ]
