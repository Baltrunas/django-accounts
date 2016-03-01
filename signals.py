import json

from django.contrib.auth.signals import user_logged_in

from .utils import join_duplicate
from .models import OrderItem


def sync_backet(sender, user, request, **kwargs):
	try:
		cookies_bucket = json.loads(request.COOKIES['cookies_bucket'])
	except:
		cookies_bucket = []

	cookies_bucket = OrderItem.objects.filter(id__in=cookies_bucket, user=None, order=None)
	server_bucket = OrderItem.objects.filter(user=user, order=None)

	join_duplicate(cookies_bucket)
	join_duplicate(server_bucket)

	for item in cookies_bucket:
		if server_bucket.filter(user=user, order=None, content_type=item.content_type, object_id=item.object_id):
			server_item = server_bucket.get(
				user=user,
				order=None,
				content_type=item.content_type,
				object_id=item.object_id
			)
			server_item.count += item.count
			server_item.save()
			item.delete()
		else:
			item.user = user
			item.save()

user_logged_in.connect(sync_backet)
