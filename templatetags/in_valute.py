from decimal import Decimal

from django import template

from ..models import Valute

register = template.Library()


@register.filter
def in_valute(price, valute):
	try:
		valute = Valute.objects.get(slug=valute)
		if type(price) != type (Decimal):
			price = Decimal(price)
		new_price = price / valute.rate
		return new_price
	except:
		return 0
