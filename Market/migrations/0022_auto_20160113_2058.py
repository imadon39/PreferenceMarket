# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0021_auto_20160113_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('effect', models.IntegerField()),
                ('level1', models.ForeignKey(related_name='level1', to='Market.Level')),
                ('level2', models.ForeignKey(related_name='level2', to='Market.Level')),
                ('product', models.ForeignKey(to='Market.Product')),
            ],
        ),
        migrations.AddField(
            model_name='level',
            name='interaction',
            field=models.ManyToManyField(to='Market.Level', through='Market.Interaction'),
        ),
    ]
