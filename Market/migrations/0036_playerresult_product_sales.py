# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0035_newideabox_accept'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerresult',
            name='product_sales',
            field=models.FloatField(default=0),
        ),
    ]
