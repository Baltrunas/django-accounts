# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_order_promocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='active_by',
            field=models.DateField(null=True, verbose_name='Active by', blank=True),
        ),
    ]
