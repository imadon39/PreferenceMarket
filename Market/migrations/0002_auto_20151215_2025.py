# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='breakdown',
            name='attribute_name',
            field=models.CharField(default=b'', max_length=300),
        ),
        migrations.AddField(
            model_name='security',
            name='attribute_name',
            field=models.CharField(default=b'', max_length=300),
        ),
        migrations.AddField(
            model_name='securityresult',
            name='attribute_name',
            field=models.CharField(default=b'', max_length=300),
        ),
    ]
