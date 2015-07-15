import json

from django import template

from ..models import OrderItem

register = template.Library()


@register.assignment_tag(takes_context=True)
def in_bucket(context, instance):
	request = context['request']
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

	for item in bucket:
		if instance == item.content_object:
			return item.count

	return 0
