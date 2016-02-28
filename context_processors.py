from django.conf import settings

from .models import Valute
from .middleware import calculate


def bucket(request):
	context = {}

	request = calculate(request)

	# Promo
	context['promocode'] = request.promocode
	context['promocode_errors'] = request.promocode_errors

	# Bucket
	context['bucket'] = request.bucket
	context['bucket_item_count'] = request.bucket_item_count
	context['bucket_total_count'] = request.bucket_total_count

	context['promo_discount'] = '%s' % request.promo_discount
	context['promo_price'] = '%s' % request.promo_price
	context['bucket_total_retail_price'] = '%s' % request.bucket_total_retail_price
	context['bucket_total_discount_price'] = '%s' % request.bucket_total_discount_price

	context['order_price'] = request.order_price

	# Current valute
	current_valute = Valute.objects.get(slug=request.COOKIES.get('valute', settings.DEFAULT_VALUTE))
	context['current_valute'] = current_valute.slug
	context['decimal_places'] = current_valute.decimal_places

	return context
