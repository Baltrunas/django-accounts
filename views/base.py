# -*- coding: utf-8 -*-
import json
import datetime

from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import redirect
from django.shortcuts import render

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

from ..forms import SingUpForm
from ..forms import ChangePasswordForm

from ..models import User
from ..models import Order
from ..models import OrderItem
from ..forms import OrderForm, OrderItemForm
import uuid

from helpful.easy_email import mail
from helpful.sms import send_sms

from django.db.models import Sum
from decimal import Decimal

from django.conf import settings

from . import payments



def singup(request):
	context = {}
	context['title'] = _('Register')
	context['form'] = SingUpForm(request.POST or None)

	if request.POST and context['form'].is_valid():
		new_user = context['form'].save()
		context['new_user'] = new_user
		new_user.backend = 'apps.accounts.auth.EmailOrUsernameModelBackend'
		login(request, new_user)
		return redirect('/', username=new_user.username)

	return render(request, 'accounts/singup.html', context)


@login_required
def profile(request):
	context = {}
	context['title'] = _('History')
	context['orders'] = Order.objects.filter(user=request.user)
	return render(request, 'accounts/profile.html', context)


@login_required
def edit(request):
	context = {}
	context['ok'] = False
	context['form'] = ChangePasswordForm(request.POST or None)
	if context['form'].is_valid():
		if authenticate(username=request.user, password=context['form'].cleaned_data["old_password"]):
			request.user.set_password(context['form'].cleaned_data['new_password'])
			request.user.save()
			context['ok'] = True
	return render(request, 'accounts/edit.html', context)


def bucket_update(request):
	if request.POST:
		content_type = ContentType.objects.get(id=int(request.POST.get('content_type', None)))
		object_id = int(request.POST.get('object_id', None))
		count = int(request.POST.get('count', 0))

		if request.user.is_authenticated():
			order_item, created = OrderItem.objects.get_or_create(
				user=request.user,
				order=None,
				content_type=content_type,
				object_id=object_id
			)
			order_item.count = count
			order_item.save()
		else:
			try:
				cookies_bucket = json.loads(request.COOKIES['cookies_bucket'])
			except:
				cookies_bucket = []

			order_item, created = OrderItem.objects.get_or_create(
				id__in=cookies_bucket,
				user=None,
				order=None,
				content_type=content_type,
				object_id=object_id
			)
			order_item.count = count
			order_item.save()

			if created:
				cookies_bucket.append(order_item.id)

			# Fresh and delete old ids
			cookies_bucket = [oi.id for oi in OrderItem.objects.filter(id__in=cookies_bucket)]

		context = {
			'status': 'ok',
			'item_count': order_item.count,
			'item_total_price': order_item.total_discount_price()
		}

		# response = HttpResponse(context, content_type="application/json")
		response = render(request, 'accounts/bucket_update.json', context, content_type='application/json')

		if request.user.is_authenticated():
			response.delete_cookie('cookies_bucket')
		else:
			response.set_cookie('cookies_bucket', value=json.dumps(cookies_bucket), path='/')
	else:
		response = HttpResponse(json.dumps({'status': 'error'}), content_type="application/json")
	return response


def promo(request):
	referer = request.META.get('HTTP_REFERER', 'order')
	response = redirect(referer)

	if request.POST:
		if request.POST.get('promocode', None):
			response.set_cookie('promocode', value=request.POST.get('promocode', None), path='/')

		if request.POST.get('deactivate', None):
			response.delete_cookie('promocode')

	return response


def order(request):
	context = {}
	context['title'] = _('Order')


	from ..middleware import calculate
	request = calculate(request)

	bucket = request.bucket

	# Orders
	user = request.user
	order_initial = {}
	if user.is_authenticated():
		order_initial['user'] = user
		order_initial['name'] = user.first_name + ' ' + user.last_name
		order_initial['email'] = user.email
		order_initial['address'] = user.address
		order_initial['phone'] = user.phone

	order_form = OrderForm(request.POST or None, initial=order_initial)

	if request.POST and order_form.is_valid():
		new_order = order_form.save()
		new_order.guid = uuid.uuid1()

		# Why if initial?
		if user.is_authenticated():
			new_order.user = user

		for item in bucket:
			item.order = new_order
			item.save()

		new_order.retail_price = request.bucket_total_retail_price
		new_order.discount_price = request.order_price
		if request.promocode:
			new_order.promocode = request.promocode

		new_order.save()

		context['new_order'] = new_order

		# Notification E-Mail
		try:
			order_email_from = settings.ORDER_EMAIL_FROM
			subject = _('We recive your order!')
			template = 'accounts/e-mail/order'
			mail(subject, context, template, order_email_from, [new_order.email, order_email_from])
		except:
			pass

		# Notification SMS
		if settings.SMS_SEND:
			send_sms('New order: %s\n%s\n%s' % (new_order.id, new_order.name, new_order.phone))

		# Pay with selected payment method
		payment = getattr(payments, new_order.payment_method)
		return payment.pay(request, new_order.id)

	context['order_form'] = order_form

	from apps.catalog.models import Product
	context['related'] = Product.objects.filter(public=True, main=True).order_by('?')[:2]

	return render(request, 'accounts/bucket.html', context)


import os
import csv
import sys
from apps.settings import MEDIA_ROOT


def render_csv(request):
	context = {}
	data = User.objects.all()
	orders = Order.objects.all()
	export = []
	for	user in data:
		export.append(
			{
				'name': user.__unicode__(),
				'email': user.email,
				'phone': user.phone
			}
		)
	for	order in orders:
		export.append(
			{
				'name': order.name,
				'email': order.email,
				'phone': order.phone,
			}
		)
	path = os.path.join(MEDIA_ROOT, 'aaa.csv')
	with open(path, 'w') as csvfile:
		try:
			writer = csv.DictWriter(csvfile, export, delimiter=",")
			writer.writeheader()
			writer.writerows(export)
			answer = True
		except Exception:
			answer = str(sys.exc_info())
		csvfile.close()
	context['export'] = export
	return HttpResponse(json.dumps(context, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")