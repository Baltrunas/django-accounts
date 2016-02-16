# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20160215_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promo',
            name='active_by',
        ),
        migrations.RemoveField(
            model_name='promo',
            name='number',
        ),
        migrations.RemoveField(
            model_name='promo',
            name='registered_users',
        ),
        migrations.RemoveField(
            model_name='promo',
            name='used',
        ),
        migrations.RemoveField(
            model_name='promo',
            name='users_limit',
        ),
        migrations.AddField(
            model_name='promo',
            name='active_after',
            field=models.DateField(null=True, verbose_name='Active after', blank=True),
        ),
        migrations.AddField(
            model_name='promo',
            name='code',
            field=models.CharField(default=1, max_length=16, verbose_name='Code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='promo',
            name='delete',
            field=models.BooleanField(default=False, verbose_name='Delete'),
        ),
        migrations.AddField(
            model_name='promo',
            name='limit',
            field=models.DecimalField(default=1, verbose_name='Limit', max_digits=60, decimal_places=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='promo',
            name='oneperuser',
            field=models.BooleanField(default=False, verbose_name='Oneperuser'),
        ),
        migrations.AddField(
            model_name='promo',
            name='only_registered',
            field=models.BooleanField(default=False, verbose_name='Only registered users'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='discount_type',
            field=models.CharField(max_length=10, choices=[(b'interest', 'Interest'), (b'percent', 'Percent')]),
        ),
    ]
