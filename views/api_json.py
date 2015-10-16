import json

from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from apps.catalog.models import Product
from ..models import Order, OrderItem
from ..forms import OrderForm, OrderItemAddForm, OrderItemForm


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
	order = Order.objects.get(id=id, acceptor=request.user, accounting=False)
	order.status = status
	order.save()

	context['status'] = 'ok'
	return HttpResponse(json.dumps(context, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")


def json_order_update(request, id):
	context = {}
	instance = Order.objects.get(id=id)
	form = OrderForm(request.POST or None, instance=instance)
	if form.is_valid():
		form.save()
		context['status'] = True
	else:
		context['status'] = False
		context['errors'] = form.errors
	return HttpResponse(json.dumps(context, ensure_ascii=False), content_type="application/json; charset=utf-8")


def json_order_item_update(request, id):
	context = {}
	instance = OrderItem.objects.get(id=id)
	form = OrderItemForm(request.POST or None, instance=instance)
	if form.is_valid():
		form.save()
		context['status'] = True
	else:
		context['status'] = False
		context['errors'] = form.errors
	return HttpResponse(json.dumps(context, ensure_ascii=False), content_type="application/json; charset=utf-8")


def json_order_item_add(request, id):
	context = {}
	item_form = OrderItemAddForm(request.POST or None)
	order = Order.objects.get(id=id)
	if item_form.is_valid():
		order_item = item_form.save(commit=False)
		content_type = ContentType.objects.get_for_model(Product)
		order_item.order = Order.objects.get(id=id)
		order_item.content_type = content_type
		order_item.save()
		order.save()
		context['status'] = True
	else:
		context['status'] = False
	return HttpResponse(json.dumps(context, ensure_ascii=False, indent=4), content_type="application/json; charset=utf-8")


def json_order_item_delete(request, id):
	context = {}
	try:
		del_orderitem = OrderItem.objects.get(id=id)
		del_orderitem.delete()
		context['status'] = True
	except:
		context['status'] = False
	return HttpResponse(json.dumps(context))