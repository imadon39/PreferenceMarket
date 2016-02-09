# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0019_auto_20160113_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('effect', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='area',
            name='age_lower',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='area',
            name='age_upper',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='number',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='breakdown',
            name='left',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='breakdown',
            name='sell',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='breakdown',
            name='selling_price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='level',
            name='number',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='market',
            name='market_number',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='market',
            name='trade_amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='market_number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='player_number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='security_number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='security',
            name='number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AddField(
            model_name='interaction',
            name='level1',
            field=models.ForeignKey(related_name='level1', to='Market.Level'),
        ),
        migrations.AddField(
            model_name='interaction',
            name='level2',
            field=models.ForeignKey(related_name='level2', to='Market.Level'),
        ),
        migrations.AddField(
            model_name='level',
            name='interaction',
            field=models.ManyToManyField(to='Market.Level', through='Market.Interaction'),
        ),
    ]
