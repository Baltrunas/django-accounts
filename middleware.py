# -*- coding: utf-8 -*-
from decimal import Decimal
from datetime import date

from django.db.models import Sum

from .models import Promo
from .models import OrderItem


class Bucket(object):
	def process_request(self, request):
		# Promo Code
		current_promo = None
		promo_errors = []
		if 'current_promo' in request.COOKIES:
			try:
				current_promo = Promo.objects.get(code=request.COOKIES['current_promo'])

				if not current_promo.active:
					promo_errors.append('Промокод не активен')

				if current_promo.active_after > date.today():
					promo_errors.append('Промокод начинает действовать с %s' % current_promo.active_after)

				if current_promo.active_before < date.today():
					promo_errors.append('Промокод прекратил действовать с %s' % current_promo.active_before)

				if current_promo.only_registered and request.user.is_anonymous():
					promo_errors.append('Промокод действителен только для зарегестрированных пользоывателей')

				if current_promo.oneperuser and request.user.is_authenticated() and current_promo.used_by_user(request.user):
					promo_errors.append('Вы уже использовали этот промокод')

				if current_promo.limit and current_promo.limit <= current_promo.used_count():
					promo_errors.append('Лимит использования этого промокода исчерпан')

			except:
				promo_errors.append('Промокод не существует')

		request.current_promo = current_promo
		request.promo_errors = promo_errors


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
		else:
			bucket = cookies_bucket


		# количество видов в корзине
		bucket_item_count = bucket.count()

		# количество товаров в корзине
		bucket_count = bucket.aggregate(Sum('count'))
		if bucket_count['count__sum']:
			bucket_total_count = bucket_count['count__sum']
		else:
			bucket_total_count = 0


		# total_price
		bucket_total_price = Decimal('0')
		for item in bucket:
			bucket_total_price += item.get_total_retail_price()

		# total_price_with_discount
		bucket_total_price_with_discount = Decimal('0')
		for item in bucket:
			bucket_total_price_with_discount += item.get_total_retail_price_with_discount()


		promo_discount = 0
		promo_price = 0
		# total_price_with_discount+promo_discount
		if current_promo and not promo_errors:
			total_item_price = Decimal('0')
			total_ditem_price = Decimal('0')

			for item in bucket:
				item_price = item.get_total_retail_price()
				item_dprice = item.get_total_retail_price_with_discount()
				if item_price > item_dprice:
					total_item_price += item_price
				else:
					total_ditem_price += item_dprice


			if current_promo.discount_type == 'interest':
				if current_promo.sum_up:
					total_price = total_item_price + total_ditem_price
					if total_price > current_promo.discount_value:
						promo_price = total_price - current_promo.discount_value
						promo_discount = current_promo.discount_value
					else:
						promo_discount = total_price
						promo_price = Decimal('0')
				else:
					if total_item_price > current_promo.discount_value:
						total_item_price = total_item_price - current_promo.discount_value
						promo_discount = current_promo.discount_value
					else:
						total_item_price = Decimal('0')
						promo_discount = total_item_price

					promo_price = total_item_price + total_ditem_price


			elif current_promo.discount_type == 'percent':
				if current_promo.sum_up:
					promo_discount = bucket_total_price_with_discount / 100 * current_promo.discount_value
				else:
					promo_discount = total_item_price / 100 * current_promo.discount_value

				promo_price = bucket_total_price_with_discount - promo_discount


		request.bucket = bucket

		request.promo_discount = promo_discount
		request.promo_price = promo_price

		request.bucket_total_price = bucket_total_price
		request.bucket_total_price_with_discount = bucket_total_price_with_discount

		request.bucket_item_count = bucket_item_count
		request.bucket_total_count = bucket_total_count

		return

	def process_response(self, request, response):
		if request.user.is_authenticated() and 'cookies_bucket' in request.COOKIES:
			response.delete_cookie('cookies_bucket')

		return response
