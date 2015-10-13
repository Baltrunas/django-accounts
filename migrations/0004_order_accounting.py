# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20151007_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='accounting',
            field=models.BooleanField(default=False, verbose_name='Accounting'),
        ),
    ]
