# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0008_auto_20160109_1640'),
    ]

    operations = [
        migrations.RenameField(
            model_name='security',
            old_name='lot',
            new_name='add_cost',
        ),
    ]
