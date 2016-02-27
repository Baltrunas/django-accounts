from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render

from ...models import Order


def pay(request, id):
	context = {}
	order = Order.objects.get(id=id)
	order.payment_status = 'processed'
	order.save()
	context['title'] = _('Cash payment')
	return render(request, 'payments/cash.html', context)
