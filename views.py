# -*- coding: utf-8 -*-
import json

from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import redirect
from django.shortcuts import render

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

from .forms import SingUpForm
from .forms import ChangePasswordForm

from .models import User
from .models import Order
from .models import OrderItem


def singup(request):
	context = {}
	context['title'] = _('Register')
	context['form'] = SingUpForm(request.POST or None)

	if request.POST and context['form'].is_valid():
		new_user = context['form'].save()
		context['new_user'] = new_user
		new_user.backend = 'django.contrib.auth.backends.ModelBackend'
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
		count = int(request.POST.get('count', None))

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
			if 'cookies_bucket' in request.COOKIES:
				try:
					cookies_bucket = json.loads(request.COOKIES['cookies_bucket'])
				except:
					cookies_bucket = []
			else:
				cookies_bucket = []

			order_items = OrderItem.objects.filter(
				id__in=cookies_bucket,
				user=None,
				order=None,
				content_type=content_type,
				object_id=object_id
			)

			if order_items:
				order_item = order_items[0]
				order_item.count = count
				order_item.save()
			else:
				order_item = OrderItem(
					content_type=content_type,
					object_id=object_id,
					count=count
				)
				order_item.save()
				cookies_bucket.append(order_item.id)

		if request.user.is_authenticated():
			bucket = OrderItem.objects.filter(user=request.user.id, order=None)
		else:
			bucket = OrderItem.objects.filter(id__in=cookies_bucket, user=None, order=None)

		bucket_total = Decimal('0')
		for item in bucket:
			bucket_total += item.get_total_retail_price_with_discount()

		bucket_count = bucket.aggregate(Sum('count'))

		if count:
			item_count = order_item.count
			item_total_price = order_item.content_object.retail_price_with_discount * order_item.count
		else:
			item_count = 0
			item_total_price = 0

		context = {
			'status': 'ok',
			'item_count': item_count,
			'item_total_price': '%s' % item_total_price,

			'bucket_total_count': bucket_count['count__sum'],
			'bucket_total_price': '%s' % bucket_total
		}

		response = HttpResponse(json.dumps(context), content_type="application/json")
		if not request.user.is_authenticated():
			response.set_cookie('cookies_bucket', value=json.dumps(cookies_bucket), path='/')
	else:
		response = HttpResponse(json.dumps({'status': 'error'}), content_type="application/json")
	return response


from django.db.models import Sum
from decimal import Decimal


def bucket(request):
	context = {}
	context['title'] = _('Bucket')

	OrderItem.objects.filter(order=None, count=0).delete()

	if request.user.is_authenticated():
		if 'cookies_bucket' in request.COOKIES:
			try:
				cookies_bucket = json.loads(request.COOKIES['cookies_bucket'])
			except:
				cookies_bucket = []

			cookies_bucket = OrderItem.objects.filter(id__in=cookies_bucket)
			server_bucket = OrderItem.objects.filter(user=request.user.id, order=None)

			for item in cookies_bucket:
				if server_bucket.filter(user=request.user, order=None, content_type=item.content_type, object_id=item.object_id):
					server_item = server_bucket.get(
						user=request.user,
						order=None,
						content_type=item.content_type,
						object_id=item.object_id
					)
					server_item.count += item.count
					server_item.save()
					item.delete()
				else:
					item.user = request.user
					item.save()

		context['bucket'] = OrderItem.objects.filter(user=request.user.id, order=None)

		response = render(request, 'accounts/bucket.html', context)
		response.delete_cookie('cookies_bucket')

	else:
		try:
			cookies_bucket = json.loads(request.COOKIES['cookies_bucket'])
		except:
			cookies_bucket = []

		context['bucket'] = OrderItem.objects.filter(id__in=cookies_bucket, user=None, order=None)
		response =  render(request, 'accounts/bucket.html', context)

	return response

from .forms import OrderForm
import uuid

from apps.useful.easy_email import mail

from django.conf import settings

def order(request):
	context = {}
	context['title'] = _('Order')

	if request.user.is_authenticated():
		bucket = OrderItem.objects.filter(user=request.user.id, order=None)
		initial = {
			'user': request.user,
			'name': request.user.first_name + ' ' + request.user.last_name,
			'email': request.user.email,
			'address': request.user.address,
			'phone': request.user.phone
		}
	else:
		if 'cookies_bucket' in request.COOKIES:
			try:
				cookies_bucket = json.loads(request.COOKIES['cookies_bucket'])
			except:
				cookies_bucket = []
		else:
			cookies_bucket = []

		bucket = OrderItem.objects.filter(id__in=cookies_bucket, user=None, order=None)
		initial = {}

	form = OrderForm(request.POST or None, initial=initial)

	if request.POST and form.is_valid():
		new_order = form.save()

		new_order.guid = uuid.uuid1()

		if request.user.is_authenticated():
			new_order.user = request.user

		for item in bucket:
			item.order = new_order
			item.save()

		new_order.save()

		context['new_order'] = new_order
		order_email_from = settings.ORDER_EMAIL_FROM
		subject = _('We recive your order!')
		template = 'accounts/e-mail/order'

		mail(subject, context, template, order_email_from, [new_order.email, order_email_from])


		context['status'] = 'ok'

	context['form'] = form

	return render(request, 'accounts/order.html', context)


from django.views.decorators.csrf import csrf_exempt
import xmltodict

@csrf_exempt
def orders_list(request):
	context = {}
	if settings.DIRECT_TO_1C:
		context['orders'] = Order.objects.filter(accounting=False)
	else:
		context['orders'] = Order.objects.filter(status='accept', accounting=False)

	return render(request, 'accounts/orders_list.xml', context, content_type="application/xhtml+xml")


@csrf_exempt
def orders_update(request):
	context = {}
	return render(request, 'accounts/orders_update.xml', context, content_type="application/xhtml+xml")


@csrf_exempt
def orders_confirm(request):
	xml_requst = xmltodict.parse(request.body)
	orders = xml_requst['hashs']['hash']

	for order_data in orders:
		guid = order_data['@guid']
		try:
			order = Order.objects.get(guid=guid)
			order.accounting = True
			order.save()
		except:
			pass
	return render(request, 'accounts/orders_confirm.xml', {}, content_type="application/xhtml+xml")

############
# API JSON #
############

def auth_check(view):
	def wrapped(request, *args, **kwargs):
		# username = request.POST.get('username', None)
		# password = request.POST.get('password', None)
		# try:
		# 	user = User.objects.get(username=username)
		# 	status = user.check_password(password)
		# except:
		# 	return HttpResponse(json.dumps({'auth': False}), content_type='application/json')
		return view(request, *args, **kwargs)
	return wrapped


@csrf_exempt
@auth_check
def json_check(request):
	return HttpResponse(json.dumps({'auth': True}), content_type='application/json')


@csrf_exempt
@auth_check
def json_order_list(request, status):
	context = {}
	context['auth'] = True

	if status == 'new':
		status_in = ['new']
	elif status == 'my':
		status_in = ['accept', 'processed', 'paid']
	elif status == 'history':
		status_in = ['success', 'canceled']

	orders = []
	for order in Order.objects.filter(status__in=status_in):
		order_items = []
		for order_item in order.items.all():
			order_item_dict = {
				"id": order_item.id,
				"name": u'%s' % order_item.content_object,
				"price": '%s' % order_item.retail_price_with_discount,
				"count": order_item.count
			}
			order_items.append(order_item_dict)

		order_dict = {
			"id": order.id,
			"name": order.name,
			"phone": order.phone,
			"status": order.status,
			"address": order.address,
			"comment": order.comment,
			"accounting": order.accounting,
			"total": '%s' % order.retail_price_with_discount,
			"created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
			"order_items": order_items
		}
		orders.append(order_dict)
	context['orders'] = orders
	return HttpResponse(json.dumps(context, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")


@csrf_exempt
def json_order_accept(request, id):
	context = {}
	id = 3

	order = Order.objects.get(id=id)
	if order.status == 'new':
		order.status = 'accept'
		order.acceptor = request.user
		order.save()
		context['status'] = 'ok'
	else:
		context['status'] = order.status
		context['acceptor'] = '%s' % order.acceptor
	return HttpResponse(json.dumps(context, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")


@csrf_exempt
def json_order_update(request, id):
	id = 3
	# имя
	# адрес
	# телефон
	# коментарий

	order = Order.objects.get(id=id, acceptor=request.user, accounting=False)
	context = {}


@csrf_exempt
def json_order_accounting(request, id):
	context = {}
	order = Order.objects.get(id=id, acceptor=request.user, accounting=False)
	order.accounting = True
	order.save()
	context['status'] = 'ok'
	return HttpResponse(json.dumps(context, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")


@csrf_exempt
def json_order_status(request, status, id):
	context = {}
	order = Order.objects.get(id=order_id, acceptor=request.user, accounting=False)
	order.status = status
	order.save()

	context['status'] = 'ok'
	return HttpResponse(json.dumps(context, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")

# new		my				canceled		success
		# processed
		# paid

# new
# accept


# http://www.dominopizza.kg/api/json/order/list/new/ (новые)
# http://www.dominopizza.kg/api/json/order/list/my/ (мои)
# http://www.dominopizza.kg/api/json/order/list/history/ (история)


# новые
	# принять
# мои
	# изменить
	# отправить в 1с
	# установить стаус
		# в процессе processed
		# оплачен paid
		# выполнен success
# история

