# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_valute'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default=b'service', max_length=b'64', verbose_name='Payment method', choices=[(b'cacshe', 'Cache'), (b'courier', 'Courier'), (b'bonus', 'Bonus'), (b'robokassa', 'Robokassa'), (b'mobilnik.kg', 'Mobilnik.kg'), (b'elsom', 'Elsom')]),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(default=b'created', max_length=32, verbose_name='Payment status', choices=[(b'created', 'Created'), (b'failed', 'Failed'), (b'processed', 'Processed'), (b'success', 'Success'), (b'canceled', 'Canceled'), (b'error', 'Error')]),
        ),
    ]
