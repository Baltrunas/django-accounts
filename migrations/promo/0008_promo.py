# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20151016_0728'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=16, verbose_name='Coupon number')),
                ('name', models.CharField(max_length=256, verbose_name='Coupon name')),
                ('description', models.TextField(verbose_name='Description')),
                ('discount_type', models.CharField(max_length=10, choices=[(b'absolute', b'Absolute'), (b'interest', b'Interest')])),
                ('discount_value', models.DecimalField(verbose_name='Value discout', max_digits=10, decimal_places=0)),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('active_before', models.DateField(verbose_name='Active before')),
                ('used', models.BooleanField(default=False, verbose_name='Used')),
                ('order', models.ForeignKey(related_name='order_promo', verbose_name='Order', to='accounts.Order')),
            ],
            options={
                'verbose_name': 'Promo',
                'verbose_name_plural': 'Promo',
            },
        ),
    ]
