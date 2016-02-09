# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0010_securityprice_share'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='lot_setting',
            new_name='cost_setting',
        ),
    ]
