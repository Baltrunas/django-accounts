# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20160227_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='promocode',
            field=models.ForeignKey(related_name='orders', verbose_name='Promo Code', blank=True, to='accounts.PromoCode', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default=b'cacshe', max_length=b'64', verbose_name='Payment method', choices=[(b'cash', b'Cash'), (b'sys_robokassa', b'Robokassa'), (b'mobilnik', b'Mobilnik'), (b'demidbank', b'DemirBank')]),
        ),
    ]
