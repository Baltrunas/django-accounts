# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20160227_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='wholesale_price',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='wholesale_price',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default=b'cash', max_length=b'64', verbose_name='Payment method', choices=[(b'cash', b'Cash'), (b'sys_robokassa', b'Robokassa'), (b'mobilnik', b'Mobilnik'), (b'demidbank', b'DemirBank')]),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='discount_type',
            field=models.CharField(max_length=10, verbose_name='Discout type', choices=[(b'interest', 'Interest'), (b'percent', 'Percent')]),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='discount_value',
            field=models.DecimalField(verbose_name='Discout value', max_digits=10, decimal_places=0),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Name'),
        ),
    ]
