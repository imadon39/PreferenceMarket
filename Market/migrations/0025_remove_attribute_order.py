# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0024_product_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='order',
        ),
    ]
