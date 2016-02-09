# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0025_remove_attribute_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Designer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='newideabox',
            name='player',
        ),
        migrations.AddField(
            model_name='designer',
            name='newidea',
            field=models.ForeignKey(to='Market.NewIdeaBox'),
        ),
        migrations.AddField(
            model_name='designer',
            name='player',
            field=models.ForeignKey(to='Market.Player'),
        ),
        migrations.AddField(
            model_name='newideabox',
            name='designers',
            field=models.ManyToManyField(to='Market.Player', through='Market.Designer'),
        ),
    ]
