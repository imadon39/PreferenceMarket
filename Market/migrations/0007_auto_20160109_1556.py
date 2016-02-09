# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0006_pricehistory_securityresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estimate_time', models.DateTimeField(verbose_name=b'estimate_time')),
                ('pricehistory', models.ForeignKey(to='Market.PriceHistory')),
            ],
        ),
        migrations.RemoveField(
            model_name='securityresult',
            name='history',
        ),
        migrations.AddField(
            model_name='history',
            name='result',
            field=models.ForeignKey(to='Market.SecurityResult'),
        ),
        migrations.AddField(
            model_name='securityresult',
            name='histories',
            field=models.ManyToManyField(to='Market.PriceHistory', through='Market.History'),
        ),
    ]
