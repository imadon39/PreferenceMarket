# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import Market.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=1, choices=[(b'f', b'Female'), (b'm', b'Male'), (b'a', b'all')])),
                ('gender_img_url', models.CharField(default=b'/static/images/gender', max_length=100)),
                ('age_lower', models.IntegerField()),
                ('age_upper', models.IntegerField()),
                ('attribute', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('number', models.IntegerField(default=0)),
                ('level_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Breakdown',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=200)),
                ('attributes', Market.models.ListField(default=[])),
                ('selling_price', models.IntegerField()),
                ('left', models.IntegerField()),
                ('sell', models.IntegerField()),
                ('sale', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('number', models.IntegerField(default=0)),
                ('attribute', models.ForeignKey(to='Market.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='LMSR',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('b', models.FloatField(default=0)),
                ('P0', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('close_time', models.DateTimeField(verbose_name=b'close time')),
                ('open_time', models.DateTimeField(verbose_name=b'open time')),
                ('name', models.CharField(max_length=200)),
                ('name_setting', models.BooleanField(default=False)),
                ('market_number', models.IntegerField(default=1)),
                ('trade_amount', models.IntegerField(default=0)),
                ('reward_setting', models.BooleanField(default=False)),
                ('GA_setting', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NewChromosome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attributes', Market.models.ListField(default=[])),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.ForeignKey(to='Market.Area')),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reward_checked', models.BooleanField(default=True)),
                ('market', models.ForeignKey(to='Market.Market')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('point', models.FloatField()),
                ('age', models.IntegerField()),
                ('number', models.IntegerField(default=0)),
                ('gender', models.CharField(max_length=1, choices=[(b'f', b'Female'), (b'm', b'Male'), (b'n', b'none')])),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('investment', models.FloatField(default=0)),
                ('sales', models.FloatField(default=0)),
                ('checked', models.BooleanField(default=False)),
                ('estimate', models.BooleanField(default=False)),
                ('estimate_time', models.DateTimeField(verbose_name=b'estimate time')),
                ('market', models.ForeignKey(to='Market.Market')),
                ('player', models.ForeignKey(to='Market.Player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerSecurity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('player', models.ForeignKey(to='Market.Player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('security_number', models.IntegerField(default=0)),
                ('amount', models.IntegerField(default=0)),
                ('action', models.CharField(max_length=10, blank=True)),
                ('cost', models.FloatField(default=0)),
                ('market', models.ForeignKey(to='Market.Market', null=True)),
                ('player', models.OneToOneField(to='Market.Player')),
            ],
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', Market.models.ListField(default=[])),
                ('market', models.OneToOneField(to='Market.Market')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('open_time', models.DateTimeField(verbose_name=b'open time')),
                ('close_time', models.DateTimeField(verbose_name=b'close time')),
                ('start_time', models.DateTimeField(verbose_name=b'start time')),
                ('end_time', models.DateTimeField(verbose_name=b'end time')),
                ('genetic_setting', models.BooleanField(default=False)),
                ('lot_setting', models.BooleanField(default=False)),
                ('maltiple_market', models.BooleanField(default=False)),
                ('market_number', models.IntegerField()),
                ('security_number', models.IntegerField()),
                ('create_idea', models.BooleanField()),
                ('area', models.ForeignKey(to='Market.Area')),
            ],
        ),
        migrations.CreateModel(
            name='RetailStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('area', models.ForeignKey(to='Market.Area')),
            ],
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=200, blank=True)),
                ('selling_price', models.IntegerField(null=True)),
                ('lot', models.IntegerField(default=0)),
                ('attributes', Market.models.ListField(default=[], blank=True)),
                ('VWAP_price', models.FloatField(default=0)),
                ('number', models.IntegerField()),
                ('VWAP_amount', models.IntegerField(default=0)),
                ('market', models.ForeignKey(to='Market.Market')),
            ],
        ),
        migrations.CreateModel(
            name='SecurityPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', Market.models.ListField(default=[], blank=True)),
                ('amount', Market.models.ListField(default=[], blank=True)),
                ('market', models.OneToOneField(to='Market.Market')),
            ],
        ),
        migrations.CreateModel(
            name='SecurityResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=200)),
                ('attributes', Market.models.ListField(default=[], blank=True)),
                ('last_price_result', models.FloatField(default=0)),
                ('VWAP_result', models.FloatField(default=0)),
                ('number', models.IntegerField()),
                ('GA_setting', models.BooleanField(default=False)),
                ('estimate_time', models.DateTimeField(verbose_name=b'estimate_time')),
                ('product', models.ForeignKey(to='Market.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ShopColor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('img_url', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ShopFigure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('img_url', models.CharField(default=b'/static/images/Shops', max_length=100)),
                ('color', models.ManyToManyField(to='Market.ShopColor')),
            ],
        ),
        migrations.AddField(
            model_name='retailstore',
            name='color',
            field=models.ForeignKey(to='Market.ShopColor'),
        ),
        migrations.AddField(
            model_name='retailstore',
            name='figure',
            field=models.ForeignKey(to='Market.ShopFigure'),
        ),
        migrations.AddField(
            model_name='retailstore',
            name='player',
            field=models.ForeignKey(to='Market.Player'),
        ),
        migrations.AddField(
            model_name='playersecurity',
            name='security',
            field=models.ForeignKey(to='Market.Security'),
        ),
        migrations.AddField(
            model_name='participation',
            name='player',
            field=models.ForeignKey(to='Market.Player'),
        ),
        migrations.AddField(
            model_name='owner',
            name='player',
            field=models.ForeignKey(to='Market.Player'),
        ),
        migrations.AddField(
            model_name='newchromosome',
            name='product',
            field=models.ForeignKey(to='Market.Product'),
        ),
        migrations.AddField(
            model_name='market',
            name='participations',
            field=models.ManyToManyField(to='Market.Player', through='Market.Participation'),
        ),
        migrations.AddField(
            model_name='market',
            name='product',
            field=models.ForeignKey(to='Market.Product'),
        ),
        migrations.AddField(
            model_name='lmsr',
            name='product',
            field=models.OneToOneField(to='Market.Product'),
        ),
        migrations.AddField(
            model_name='breakdown',
            name='result',
            field=models.ForeignKey(to='Market.PlayerResult'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='product',
            field=models.ForeignKey(to='Market.Product'),
        ),
        migrations.AddField(
            model_name='area',
            name='owners',
            field=models.ManyToManyField(to='Market.Player', through='Market.Owner'),
        ),
    ]
