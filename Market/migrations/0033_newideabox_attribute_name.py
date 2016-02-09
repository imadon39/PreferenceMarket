# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0032_remove_newideabox_attribute_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='newideabox',
            name='attribute_name',
            field=models.CharField(default=b'', max_length=300),
        ),
    ]
