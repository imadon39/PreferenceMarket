# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0017_auto_20160113_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='LMSR',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('b', models.FloatField(default=0)),
                ('P0', models.FloatField(default=0)),
                ('product', models.OneToOneField(to='Market.Product')),
            ],
        ),
    ]
