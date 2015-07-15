import json
from decimal import Decimal

from django.db.models import Sum

from .models import OrderItem


def bucket(request):
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


	return {
		'bucket_total_count': bucket_total_count,
		'bucket_total_price': '%s' % bucket_total,
	}
