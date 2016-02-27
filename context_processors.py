from .models import Valute


def bucket(request):
	context = {}

	# Promo
	context['promocode'] = request.promocode
	context['promocode_errors'] = request.promocode_errors

	# Bucket
	context['bucket'] = request.bucket
	context['bucket_item_count'] = request.bucket_item_count
	context['bucket_total_count'] = request.bucket_total_count

	context['promo_discount'] = '%s' % request.promo_discount
	context['promo_price'] = '%s' % request.promo_price
	context['bucket_total_price'] = '%s' % request.bucket_total_price
	context['bucket_total_price_with_discount'] = '%s' % request.bucket_total_price_with_discount

	# Current valute
	current_valute = Valute.objects.get(slug=request.COOKIES.get('valute', 'kgs'))
	context['current_valute'] = current_valute.slug
	context['decimal_places'] = current_valute.decimal_places

	return context
