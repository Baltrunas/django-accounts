from django.conf.urls import url
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.utils.translation import ugettext_lazy as _

from .forms import EmailAuthenticationForm

from . import views
from views import api_json

urlpatterns = [
	url(r'^singup/$', views.base.singup, name='singup'),

	url(r'^login/$',auth_views.login, {'authentication_form': EmailAuthenticationForm},name='login'),
	url(r'^logout/$', auth_views.logout_then_login, name='logout'),
	url(r'^password_change/$', auth_views.password_change, name='password_change'),
	url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
	url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
	url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
	url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

	url(r'^profile/$', views.base.profile, name='profile'),
	url(r'^profile/edit/$', views.base.edit, name='accounts_edit'),

	url(r'^bucket/update/$', views.base.bucket_update, name='bucket_update'),

	url(r'^promo/$', views.base.promo, name='accounts_promo'),

	url(r'^order/$', views.base.order, name='order'),


	# PAY
	# url(r'^pay/mobilnik/$', views.pay.pay_mobilnik, name="pay_mobilnik"),
	# url(r'^pay/robokassa/', include('robokassa.urls')),

	# API XML
	url(r'^api/xml/orders/list/$', views.api_xml.orders_list, name='orders_list'),
	url(r'^api/xml/orders/update/$', views.api_xml.orders_update, name='orders_update'),
	url(r'^api/xml/orders/confirm/$', views.api_xml.orders_confirm, name='orders_confirm'),

	# API JSON
	url(r'^api/json/category/list/$', views.api_json.json_category_list, name='json_category_list'),
	url(r'^api/json/category/add/$', views.api_json.json_category_add, name='json_category_add'),
	url(r'^api/json/category/update/(?P<category_id>\d+)/$', views.api_json.json_category_update, name='json_category_update'),
	url(r'^api/json/category/delete/(?P<category_id>\d+)/$', views.api_json.json_category_delete, name='json_category_delete'),

	url(r'^api/json/check/$', views.api_json.json_check, name='json_check'),
	url(r'^api/json/order/list/(?P<status>new|my|history)/$', views.api_json.json_order_list, name='json_order_list'),
	url(r'^api/json/order/accept/(?P<order_id>[0-9]+)/$', views.api_json.json_order_accept, name='json_order_accept'),
	url(r'^api/json/order/update/(?P<order_id>\d+)/$', api_json.json_order_update, name='json_order_update'),
	url(r'^api/json/order/accounting/(?P<order_id>[0-9]+)/$', views.api_json.json_order_accounting, name='json_order_accounting'),
	url(r'^api/json/order/status/(?P<status>processed|paid|success|canceled)/(?P<order_id>[0-9]+)/$', views.api_json.json_order_status, name='json_order_status'),

	# Items
	url(r'^api/json/order/item/add/(?P<order_id>\d+)/$', api_json.json_order_item_add, name='json_order_item_add'),
	url(r'^api/json/order/item/update/(?P<order_item_id>\d+)/$', api_json.json_order_item_update, name='json_order_item_update'),
	url(r'^api/json/order/item/delete/(?P<order_item_id>\d+)/$', api_json.json_order_item_delete, name='json_order_item_delete'),



	url(r'^ren/$', views.base.render_csv, name='ren'),
]
