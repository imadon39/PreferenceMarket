# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0034_auto_20160115_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='newideabox',
            name='accept',
            field=models.BooleanField(default=False),
        ),
    ]
