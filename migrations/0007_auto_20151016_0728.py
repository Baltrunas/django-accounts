# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20151014_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='valute',
            name='decimal_places',
            field=models.PositiveIntegerField(default=0, verbose_name='Decimal places'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default=b'cacshe', max_length=b'64', verbose_name='Payment method', choices=[(b'cacshe', 'Cache'), (b'courier', 'Courier'), (b'bonus', 'Bonus'), (b'robokassa', 'Robokassa'), (b'mobilnik.kg', 'Mobilnik.kg'), (b'elsom', 'Elsom')]),
        ),
    ]
