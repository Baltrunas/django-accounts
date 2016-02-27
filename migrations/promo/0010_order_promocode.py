# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_promo_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='promocode',
            field=models.CharField(max_length=16, null=True, verbose_name='Promo code', blank=True),
        ),
    ]
