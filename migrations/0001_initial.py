# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=50, verbose_name='Phone')),
                ('address', models.CharField(max_length=50, null=True, verbose_name='Address', blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('email', models.EmailField(max_length=100, null=True, verbose_name='E-Mail', blank=True)),
                ('address', models.CharField(max_length=300, verbose_name='Address')),
                ('phone', models.CharField(max_length=100, verbose_name='Phone')),
                ('comment', models.TextField(null=True, verbose_name='Comment', blank=True)),
                ('retail_price', models.DecimalField(default=Decimal('0.0000'), verbose_name='Retail Price', max_digits=16, decimal_places=4)),
                ('wholesale_price', models.DecimalField(decimal_places=4, default=Decimal('0.0000'), max_digits=16, blank=True, null=True, verbose_name='Wholesale Price')),
                ('retail_price_with_discount', models.DecimalField(decimal_places=4, default=Decimal('0.0000'), max_digits=16, blank=True, null=True, verbose_name='Retail Price With Discount')),
                ('status', models.CharField(default=b'created', max_length=32, verbose_name='Status', choices=[(b'created', 'Created'), (b'processed', 'Processed'), (b'canceled', 'Canceled'), (b'success', 'Success')])),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(verbose_name='Object ID')),
                ('retail_price', models.DecimalField(default=Decimal('0.0000'), verbose_name='Retail Price', max_digits=16, decimal_places=4)),
                ('wholesale_price', models.DecimalField(decimal_places=4, default=Decimal('0.0000'), max_digits=16, blank=True, null=True, verbose_name='Wholesale Price')),
                ('retail_price_with_discount', models.DecimalField(decimal_places=4, default=Decimal('0.0000'), max_digits=16, blank=True, null=True, verbose_name='Retail Price With Discount')),
                ('count', models.IntegerField(default=0, null=True, verbose_name='Count', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('content_type', models.ForeignKey(verbose_name='Content Type', to='contenttypes.ContentType')),
                ('order', models.ForeignKey(related_name='items', verbose_name='Order', blank=True, to='accounts.Order', null=True)),
                ('user', models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
