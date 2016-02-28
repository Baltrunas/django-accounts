# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20160228_1308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='retail_price_with_discount',
            new_name='discount_price',
        ),
        migrations.AlterField(
            model_name='order',
            name='discount_price',
            field=models.DecimalField(decimal_places=4, default=Decimal('0.0000'), max_digits=16, blank=True, null=True, verbose_name='Discount price'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='retail_price',
            field=models.DecimalField(default=Decimal('0.0000'), verbose_name='Retail price', max_digits=16, decimal_places=4),
        ),
    ]
