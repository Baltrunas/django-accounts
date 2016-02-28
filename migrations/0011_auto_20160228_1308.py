# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20160228_1240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='retail_price_with_discount',
            new_name='discount_price',
        ),
    ]
