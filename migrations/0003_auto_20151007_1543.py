# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_order_guid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='acceptor',
            field=models.ForeignKey(related_name='acceptors', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='guid',
            field=models.CharField(verbose_name='GUID', max_length=37, null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'new', max_length=32, verbose_name='Status', choices=[(b'new', 'New'), (b'accept', 'Accept by:'), (b'processed', 'Processed (1c)'), (b'paid', 'Paid'), (b'success', 'Success'), (b'canceled', 'Canceled')]),
        ),
    ]
