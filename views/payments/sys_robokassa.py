from django.conf import settings
from django.shortcuts import redirect

from robokassa.forms import RobokassaForm

from robokassa.signals import result_received
from robokassa.signals import success_page_visited
from robokassa.signals import fail_page_visited

from ...models import Order
from ...models import Valute


# Payment creator views
def pay(request, id):
	order = Order.objects.get(id=id)

	CURRENCY = getattr(settings, 'ROBOKASSA_CURRENCY', False)

	if CURRENCY:
		valute = Valute.objects.get(slug=settings.ROBOKASSA_CURRENCY.lower())
		amount = order.retail_price_with_discount / valute.rate
	else:
		amount = order.retail_price_with_discount

	robokassa_form = RobokassaForm(initial={
		'OutSum': amount,
		'InvId': order.id,
		'Desc': 'Order #%s' % order.id,
		'Email': order.email,
		'Encoding': 'utf8',
		'Culture': 'ru'
	})

	return redirect(robokassa_form.get_redirect_url())


# Payment signals
def payment_received(sender, **kwargs):
	order = Order.objects.get(id=kwargs['InvId'])
	order.status = 'processed'
	order.save()

result_received.connect(payment_received)


def payment_success(sender, **kwargs):
	order = Order.objects.get(id=kwargs['InvId'])
	order.payment_status = 'success'
	order.save()

success_page_visited.connect(payment_success)


def payment_fail(sender, **kwargs):
	order = Order.objects.get(id=kwargs['InvId'])
	order.status = 'failed'
	order.save()

fail_page_visited.connect(payment_fail)
