# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='guid',
            field=models.CharField(max_length=37, null=True, verbose_name='GUID', blank=True),
        ),
    ]
