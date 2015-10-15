import json

from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render

from robokassa.forms import RobokassaForm

from ..models import Order
from ..models import Valute

# @login_required
def pay(request, id):
	context = {}
	context['title'] = _('Pay')
	order = Order.objects.get(id=id)
	context['order'] = order

	CURRENCY = getattr(settings, 'ROBOKASSA_CURRENCY', False)

	if CURRENCY:
		valute = Valute.objects.get(slug=settings.ROBOKASSA_CURRENCY.lower())
		amount = order.retail_price_with_discount / valute.rate
	else:
		amount = order.retail_price_with_discount

	form = RobokassaForm(initial={
		'OutSum': amount,
		'InvId': order.id,
		'Desc': 'Order #%s' % order.id,
		'Email': order.email,
		'Encoding': 'utf8',
		'Culture': 'ru'
	})
	context['form'] = form
	return render(request, 'accounts/pay/pay.html', context)


from robokassa.signals import result_received
from robokassa.signals import success_page_visited
from robokassa.signals import fail_page_visited

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


def pay_mobilnik(request):
	context = {}
	context['title'] = _('Pay')
	if request.POST and request.POST.get('datetime', ''):
		order = Transaction(
			amount = Decimal('0.0'),
			user = request.user,
			status = 'processed',
			comment = request.POST.get('datetime', ''),
			payment_method = 'mobilnik.kg'
		)
		order.save()

		context['ok'] = True
	else:
		context['ok'] = False
	return render(request, 'accounts/pay/mobilnik.html', context)

