import json

from decimal import Decimal
from datetime import date

from django.db.models import Sum
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from .models import PromoCode
from .models import OrderItem


def decimal_format(decimal, decimal_places):
	string = '{:.{decimal_places}f}'.format(decimal, decimal_places=decimal_places)
	return string


def join_duplicate(duplicate_set):
	duplicate_groups = duplicate_set.values('content_type', 'object_id').order_by('content_type').annotate(cc=Count('content_type'))

	unique_set = []
	for duplicate_item in duplicate_groups:
		duplicate_list = duplicate_set.filter(content_type=duplicate_item['content_type'], object_id=duplicate_item['object_id'])
		first = duplicate_list[0]
		unique_set.append(first)
		for duplicate_item in duplicate_list[1:]:
			first.count += duplicate_item.count
			first.save()
			duplicate_item.delete()

	return unique_set



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


	# Clear zero items from bucket
	OrderItem.objects.filter(order=None, count=0).delete()

	if request.user.is_authenticated():
		bucket = OrderItem.objects.filter(user=request.user.id, order=None)
	else:
		try:
			cookies_bucket = json.loads(request.COOKIES['cookies_bucket'])
		except:
			cookies_bucket = []

		bucket = OrderItem.objects.filter(id__in=cookies_bucket, user=None, order=None)

	join_duplicate(bucket)

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


	# calculate total_price_with_discount+promo_discount
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
	request.bucket_item_count = bucket_item_count
	request.bucket_total_count = bucket_total_count
	request.bucket_total_retail_price = bucket_total_retail_price
	request.bucket_total_discount_price = bucket_total_discount_price

	request.promocode = promocode
	request.promocode_errors = promocode_errors

	request.promo_discount = promo_discount
	request.promo_price = promo_price

	if request.promo_price:
		request.order_price = request.promo_price
	else:
		request.order_price = request.bucket_total_discount_price


	return request
