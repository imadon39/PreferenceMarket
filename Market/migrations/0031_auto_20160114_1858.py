# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0030_auto_20160114_1838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newideabox',
            old_name='contain_newAdd',
            new_name='contain_newAtt',
        ),
        migrations.RenameField(
            model_name='newideabox',
            old_name='newAdd',
            new_name='newAttribute',
        ),
        migrations.RenameField(
            model_name='newideabox',
            old_name='newAdd_name',
            new_name='newAttribute_name',
        ),
    ]
