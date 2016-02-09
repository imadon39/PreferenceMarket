# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0012_auto_20160113_0255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lmsr',
            name='product',
        ),
        migrations.DeleteModel(
            name='LMSR',
        ),
    ]
