# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0031_auto_20160114_1858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newideabox',
            name='attribute_name',
        ),
    ]
