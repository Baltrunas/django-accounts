# from django.utils.translation import ugettext as _
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import redirect
from django.shortcuts import render

from .forms import SingUpForm
from .forms import ChangePasswordForm
from .models import Order
from .models import OrderItem
import json
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse


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


@login_required
def change_password(request):
	context = {}
	context['ok'] = False
	context['form'] = ChangePasswordForm(request.POST or None)
	if context['form'].is_valid():
		if authenticate(username=request.user, password=context['form'].cleaned_data["old_password"]):
			request.user.set_password(context['form'].cleaned_data['new_password'])
			request.user.save()
			context['ok'] = True
	return render(request, 'accounts/change_password.html', context)




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



def bucket_add(request):
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
			order_item.count += count
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
				order_item.count += count
				order_item.save()
			else:
				order_item = OrderItem(
					user=request.user.id,
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


		item_total_price = order_item.content_object.retail_price_with_discount * order_item.count

		context = {
			'status': 'ok',
			'item_count': order_item.count,
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


def bucket_delete(request):
	if request.POST:
		id = int(request.POST.get('id', None))

	if 'cookies_bucket' in request.COOKIES:
		try:
			cookies_bucket = json.loads(request.COOKIES['cookies_bucket'])
		except:
			cookies_bucket = []
	else:
		cookies_bucket = []

	if id in cookies_bucket:
		OrderItem.objects.filter(user=None, order=None, id=id).delete()
		cookies_bucket.remove(id)

		bucket = OrderItem.objects.filter(id__in=cookies_bucket, user=None, order=None)
	if request.user.is_authenticated():
		OrderItem.objects.filter(user=request.user, order=None, id=id).delete()

		bucket = OrderItem.objects.filter(user=request.user.id, order=None)

	bucket_total = Decimal('0')
	for item in bucket:
		bucket_total += item.get_total_retail_price_with_discount()

	bucket_count = bucket.aggregate(Sum('count'))

	context = {
		'status': 'ok',
		'bucket_total_count': bucket_count['count__sum'],
		'bucket_total_price': '%s' % bucket_total
	}

	response = HttpResponse(json.dumps(context), content_type="application/json")
	if not request.user.is_authenticated():
		response.set_cookie('cookies_bucket', value=json.dumps(cookies_bucket), path='/')

	return response


def bucket_edit(request):
	if request.POST:
		id = int(request.POST.get('id', None))
		count = int(request.POST.get('count', None))

		if 'cookies_bucket' in request.COOKIES:
			try:
				cookies_bucket = json.loads(request.COOKIES['cookies_bucket'])
			except:
				cookies_bucket = []
		else:
			cookies_bucket = []

		if id in cookies_bucket:
			order_item = OrderItem.objects.get(id=id, user=None, order=None)
		elif request.user.is_authenticated():
			order_item = OrderItem.objects.get(id=id, user=request.user, order=None)



		order_item.count = count
		order_item.save()

		if request.user.is_authenticated():
			bucket = OrderItem.objects.filter(user=request.user.id, order=None)
		else:
			bucket = OrderItem.objects.filter(id__in=cookies_bucket, user=None, order=None)

		bucket_total = Decimal('0')
		for item in bucket:
			bucket_total += item.get_total_retail_price_with_discount()

		bucket_count = bucket.aggregate(Sum('count'))


		item_total_price = order_item.content_object.retail_price_with_discount * order_item.count

		context = {
			'status': 'ok',
			'item_count': order_item.count,
			'item_total_price': '%s' % item_total_price,

			'bucket_total_count': bucket_count['count__sum'],
			'bucket_total_price': '%s' % bucket_total
		}

		response = HttpResponse(json.dumps(context), content_type="application/json")
	else:
		response = HttpResponse(json.dumps({'status': 'error'}), content_type="application/json")
	return response



def bucket_sync(request):
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

	response = redirect('bucket')
	response.delete_cookie('cookies_bucket')
	return response


def bucket_clear(request):
	response = redirect('bucket')
	response.delete_cookie('cookies_bucket')
	return response


def bucket(request):
	context = {}
	context['title'] = _('Bucket')

	if request.user.is_authenticated():
		server_bucket = OrderItem.objects.filter(user=request.user.id, order=None)
		context['server_bucket'] = server_bucket

	if 'cookies_bucket' in request.COOKIES:
		try:
			cookies_bucket = json.loads(request.COOKIES['cookies_bucket'])
		except:
			cookies_bucket = []

		cookies_bucket = OrderItem.objects.filter(id__in=cookies_bucket, user=None, order=None)
		context['cookies_bucket'] = cookies_bucket

	return render(request, 'accounts/bucket.html', context)


from .forms import OrderForm




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

		if request.user.is_authenticated():
			new_order.user = request.user

		for item in bucket:
			item.order = new_order
			item.save()
		new_order = form.save()

		context['new_order'] = new_order
		order_email_from = settings.ORDER_EMAIL_FROM
		subject = _('We recive your order!')
		template = 'accounts/e-mail/order'

		mail(subject, context, template, order_email_from, [new_order.email])


		context['status'] = 'ok'

	context['form'] = form

	return render(request, 'accounts/order.html', context)
