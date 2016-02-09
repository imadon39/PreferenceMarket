# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0039_auto_20160120_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='designer',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
