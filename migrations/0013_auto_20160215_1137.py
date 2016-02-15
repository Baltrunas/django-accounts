# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20160212_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='promocode',
            field=models.ForeignKey(related_name='promocodes', verbose_name='Promo', blank=True, to='accounts.Promo', null=True),
        ),
    ]
