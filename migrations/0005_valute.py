# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_order_accounting'),
    ]

    operations = [
        migrations.CreateModel(
            name='Valute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', models.SlugField(help_text='A slug is the part of a URL which identifies a page using human-readable keywords', max_length=128, verbose_name='Slug')),
                ('rate', models.DecimalField(default=Decimal('0.0000'), verbose_name='Currency rate', max_digits=16, decimal_places=4)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Currency rate',
                'verbose_name_plural': 'Currency rates',
            },
        ),
    ]
