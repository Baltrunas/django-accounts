# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_promo_active_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='registered_users',
            field=models.BooleanField(default=False, verbose_name='registered users'),
        ),
        migrations.AddField(
            model_name='promo',
            name='sum_up',
            field=models.BooleanField(default=False, verbose_name='sum up'),
        ),
        migrations.AddField(
            model_name='promo',
            name='users_limit',
            field=models.DecimalField(default=1, verbose_name='users limit', max_digits=60, decimal_places=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='promocode',
            field=models.ForeignKey(related_name='promocodes', default=1, verbose_name='Promo', to='accounts.Promo'),
            preserve_default=False,
        ),
    ]
