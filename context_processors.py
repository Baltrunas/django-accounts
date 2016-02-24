import json
from decimal import Decimal

from django.db.models import Sum

from .models import Valute
from .models import OrderItem
from .models import Promo


def bucket(request):
	context = {}

	# Promo Code
	if 'current_promo' in request.COOKIES:
		try:
			current_promo = Promo.objects.get(
				code=request.COOKIES['current_promo'],
				active=True
				# active_after
				# active_before
			)
			context['current_promo'] = current_promo
		except:
			context['promo_error'] = True
			# request.COOKIES['current_promo'] = 'deleted'
	else:
		print 'real deleted'

	# Bucket
	if request.user.is_authenticated():
		bucket = OrderItem.objects.filter(user=request.user.id, order=None)
	else:
		if 'cookies_bucket' in request.COOKIES:
			try:
				cookies_bucket = json.loads(request.COOKIES['cookies_bucket'])
			except:
				cookies_bucket = []
		else:
			cookies_bucket = []

		bucket = OrderItem.objects.filter(id__in=cookies_bucket, user=None, order=None)

	bucket_count = bucket.aggregate(Sum('count'))
	if bucket_count['count__sum']:
		bucket_total_count = bucket_count['count__sum']
	else:
		bucket_total_count = 0

	bucket_total = Decimal('0')
	for item in bucket:
		bucket_total += item.get_total_retail_price_with_discount()


	current_valute = Valute.objects.get(slug=request.COOKIES.get('valute', 'kgs'))


	context['bucket_total_count'] = bucket_total_count
	context['bucket_total_price'] = '%s' % bucket_total
	context['current_valute'] = current_valute.slug
	context['decimal_places'] = current_valute.decimal_places

	return context
