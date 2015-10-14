import xmltodict

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def orders_list(request):
	context = {}
	if settings.DIRECT_TO_1C:
		context['orders'] = Order.objects.filter(accounting=False)
	else:
		context['orders'] = Order.objects.filter(status='accept', accounting=False)

	return render(request, 'accounts/xml/orders_list.xml', context, content_type="application/xhtml+xml")


@csrf_exempt
def orders_update(request):
	context = {}
	return render(request, 'accounts/xml/orders_update.xml', context, content_type="application/xhtml+xml")


@csrf_exempt
def orders_confirm(request):
	xml_requst = xmltodict.parse(request.body)
	orders = xml_requst['hashs']['hash']

	for order_data in orders:
		guid = order_data['@guid']
		try:
			order = Order.objects.get(guid=guid)
			order.accounting = True
			order.save()
		except:
			pass
	return render(request, 'accounts/xml/orders_confirm.xml', {}, content_type="application/xhtml+xml")
