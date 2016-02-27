# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20151016_0728'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=32, verbose_name='Code')),
                ('name', models.CharField(max_length=256, verbose_name='Coupon name')),
                ('description', models.TextField(verbose_name='Description')),
                ('discount_type', models.CharField(max_length=10, choices=[(b'interest', 'Interest'), (b'percent', 'Percent')])),
                ('discount_value', models.DecimalField(verbose_name='Value discout', max_digits=10, decimal_places=0)),
                ('limit', models.DecimalField(verbose_name='Limit', max_digits=60, decimal_places=0)),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('active_from', models.DateField(null=True, verbose_name='Active from', blank=True)),
                ('active_before', models.DateField(verbose_name='Active before')),
                ('sum_up', models.BooleanField(default=False, verbose_name='Sum up')),
                ('only_registered', models.BooleanField(default=False, verbose_name='Only registered')),
                ('one_per_user', models.BooleanField(default=False, verbose_name='One per user')),
            ],
            options={
                'verbose_name': 'Promo Code',
                'verbose_name_plural': 'Promo Codes',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='promocode',
            field=models.ForeignKey(related_name='orders', verbose_name='Promo Code', blank=True, to='accounts.PromoCode', null=True),
        ),
    ]
