import json

from decimal import Decimal
from datetime import date

from django.db.models import Sum
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from .models import PromoCode
from .models import OrderItem


def calculate(request):
	# Promo Code
	promocode = None
	promocode_errors = []
	if 'promocode' in request.COOKIES:
		try:
			promocode = PromoCode.objects.get(code=request.COOKIES['promocode'])

			if not promocode.active:
				promocode_errors.append(_('Promo code is not active'))

			if promocode.active_from > date.today():
				promocode_errors.append('%s %s' % (_('Promo code active from'), promocode.active_from))

			if promocode.active_before < date.today():
				promocode_errors.append('%s %s' % (_('Promo code active before'), promocode.active_before))

			if promocode.only_registered and request.user.is_anonymous():
				promocode_errors.append(_('Promo Code  only for registered users'))

			if promocode.one_per_user and request.user.is_authenticated() and promocode.used_by_user(request.user):
				promocode_errors.append(_('You have already used this promo code'))

			if promocode.limit and promocode.limit <= promocode.used_count():
				promocode_errors.append(_('Limit use this promo code exhausted'))

		except:
			promocode_errors.append(_('Promo code does not exist'))

	request.promocode = promocode
	request.promocode_errors = promocode_errors


	# Clear zero items from bucket
	OrderItem.objects.filter(order=None, count=0).delete()

	# Get cookies_bucket
	try:
		cookies_bucket = json.loads(request.COOKIES['cookies_bucket'])
	except:
		cookies_bucket = []

	cookies_bucket = OrderItem.objects.filter(id__in=cookies_bucket, user=None, order=None)


	if request.user.is_authenticated():
		server_bucket = OrderItem.objects.filter(user=request.user.id, order=None)

		# clear bucket bugs
		user_items_groups = server_bucket.values('content_type', 'object_id').order_by('content_type').annotate(cc=Count('content_type'))

		for user_item in user_items_groups:
			group = server_bucket.filter(content_type=user_item['content_type'], object_id=user_item['object_id'])
			first_object = group[0]
			for group_item in group[1:]:
				first_object.count += group_item.count
				first_object.save()
				group_item.delete()

		if 'cookies_bucket' in request.COOKIES:
			# Update server bucket
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

			server_bucket = OrderItem.objects.filter(user=request.user.id, order=None)

		bucket = server_bucket

		request.COOKIES.pop('cookies_bucket', None)
	else:
		# clear bucket bugs
		user_items_groups = cookies_bucket.values('content_type', 'object_id').order_by('content_type').annotate(cc=Count('content_type'))


		for user_item in user_items_groups:
			group = cookies_bucket.filter(content_type=user_item['content_type'], object_id=user_item['object_id'])
			first_object = group[0]
			for group_item in group[1:]:
				first_object.count += group_item.count
				first_object.save()
				# cookies_bucket.remove(group_item.id) # delete from
				group_item.delete()

		bucket = cookies_bucket


	# Bucket items count
	bucket_item_count = bucket.count()

	# Bucket goods count
	bucket_count = bucket.aggregate(Sum('count'))
	if bucket_count['count__sum']:
		bucket_total_count = bucket_count['count__sum']
	else:
		bucket_total_count = 0


	# total_price
	bucket_total_retail_price = Decimal('0')
	for item in bucket:
		bucket_total_retail_price += item.total_retail_price()

	# total_price_with_discount
	bucket_total_discount_price = Decimal('0')
	for item in bucket:
		bucket_total_discount_price += item.total_discount_price()


	# total_price_with_discount+promo_discount
	promo_discount = 0
	promo_price = 0
	if promocode and not promocode_errors:
		total_without_discount = Decimal('0')
		total_with_discount = Decimal('0')

		for item in bucket:
			if item.total_discount_price() < item.total_retail_price():
				total_with_discount += item.total_discount_price()
			else:
				total_without_discount += item.total_retail_price()


		if promocode.discount_type == 'interest':
			if promocode.sum_up:
				if bucket_total_discount_price > promocode.discount_value:
					promo_discount = promocode.discount_value
					promo_price = bucket_total_discount_price - promocode.discount_value
				else:
					promo_discount = bucket_total_discount_price
					promo_price = Decimal('0')
			else:
				if total_without_discount > promocode.discount_value:
					promo_discount = promocode.discount_value
					total_without_discount = total_without_discount - promocode.discount_value
				else:
					promo_discount = total_without_discount
					total_without_discount = Decimal('0')
				promo_price = total_without_discount + total_with_discount


		elif promocode.discount_type == 'percent':
			if promocode.sum_up:
				promo_discount = bucket_total_discount_price / 100 * promocode.discount_value
			else:
				print total_without_discount
				promo_discount = total_without_discount / 100 * promocode.discount_value
			promo_price = bucket_total_discount_price - promo_discount


	request.bucket = bucket

	request.promo_discount = promo_discount
	request.promo_price = promo_price

	request.bucket_total_retail_price = bucket_total_retail_price
	request.bucket_total_discount_price = bucket_total_discount_price

	request.bucket_item_count = bucket_item_count
	request.bucket_total_count = bucket_total_count

	if request.promo_price:
		request.order_price = request.promo_price
	else:
		request.order_price = request.bucket_total_discount_price


	return request


class Bucket(object):
	def process_request(self, request):
		request = calculate(request)

		return
