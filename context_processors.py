from .models import Valute


def bucket(request):
	context = {}

	# Promo
	context['current_promo'] = request.current_promo
	context['promo_errors'] = request.promo_errors

	# Bucket
	context['bucket'] = request.bucket
	# context['bucket_total_count'] = bucket_total_count
	# context['bucket_total_price'] = '%s' % bucket_total

	# Current valute
	current_valute = Valute.objects.get(slug=request.COOKIES.get('valute', 'kgs'))
	context['current_valute'] = current_valute.slug
	context['decimal_places'] = current_valute.decimal_places

	return context
