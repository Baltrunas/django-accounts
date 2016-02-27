import json

from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render


from ...models import Order
from ...models import Valute


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
