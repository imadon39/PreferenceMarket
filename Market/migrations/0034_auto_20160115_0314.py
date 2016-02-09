# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0033_newideabox_attribute_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='designer',
            old_name='newidea',
            new_name='newIdea',
        ),
    ]
