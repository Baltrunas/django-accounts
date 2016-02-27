# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20160216_1240'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promo',
            options={'verbose_name': 'Promo Code', 'verbose_name_plural': 'Promo Codes'},
        ),
        migrations.RemoveField(
            model_name='promo',
            name='active_after',
        ),
        migrations.RemoveField(
            model_name='promo',
            name='delete',
        ),
        migrations.RemoveField(
            model_name='promo',
            name='oneperuser',
        ),
        migrations.AddField(
            model_name='promo',
            name='active_from',
            field=models.DateField(null=True, verbose_name='Active from', blank=True),
        ),
        migrations.AddField(
            model_name='promo',
            name='one_per_user',
            field=models.BooleanField(default=False, verbose_name='One per user'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default=b'cacshe', max_length=b'64', verbose_name='Payment method', choices=[(b'cash', b'Cash'), (b'sys_robokassa', b'Robokassa'), (b'mobilnik', b'Mobilnik'), (b'demidbank', b'DemirBank')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='promocode',
            field=models.ForeignKey(related_name='orders', verbose_name='Promo', blank=True, to='accounts.Promo', null=True),
        ),
        migrations.AlterField(
            model_name='promo',
            name='code',
            field=models.CharField(max_length=32, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='only_registered',
            field=models.BooleanField(default=False, verbose_name='Only registered'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='sum_up',
            field=models.BooleanField(default=False, verbose_name='Sum up'),
        ),
    ]
