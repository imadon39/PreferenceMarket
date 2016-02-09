# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0038_auto_20160118_1603'),
    ]

    operations = [
        migrations.RenameField(
            model_name='breakdown',
            old_name='initial_investment',
            new_name='discount',
        ),
        migrations.RenameField(
            model_name='breakdown',
            old_name='left',
            new_name='gross_margin',
        ),
        migrations.RenameField(
            model_name='breakdown',
            old_name='sell',
            new_name='purchase_number',
        ),
        migrations.RenameField(
            model_name='breakdown',
            old_name='sale',
            new_name='sales',
        ),
        migrations.RenameField(
            model_name='playerresult',
            old_name='product_sales',
            new_name='profit_rate',
        ),
        migrations.RenameField(
            model_name='playerresult',
            old_name='sales',
            new_name='total_sales',
        ),
        migrations.RenameField(
            model_name='securityprice',
            old_name='share',
            new_name='sale_rate',
        ),
        migrations.RemoveField(
            model_name='breakdown',
            name='mean_sale_rate',
        ),
        migrations.RemoveField(
            model_name='breakdown',
            name='total',
        ),
        migrations.RemoveField(
            model_name='designer',
            name='checked',
        ),
        migrations.AddField(
            model_name='security',
            name='gross_margin',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='securityresult',
            name='sale_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='breakdown',
            name='sale_rate',
            field=models.FloatField(),
        ),
    ]
