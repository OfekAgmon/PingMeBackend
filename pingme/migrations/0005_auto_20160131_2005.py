# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('pingme', '0004_auto_20160131_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.DecimalField(default=Decimal('0.00'), decimal_places=7, max_digits=10),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.DecimalField(default=Decimal('0.00'), decimal_places=7, max_digits=10),
        ),
    ]
