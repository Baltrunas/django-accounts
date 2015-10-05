from django.conf.urls import url
# , include

from django.utils.translation import ugettext_lazy as _

from . import views
from .forms import EmailAuthenticationForm


urlpatterns = [
	# url('^', include('django.contrib.auth.urls')),
	url(
		r'^login/$',
		'django.contrib.auth.views.login',
		{
			'template_name': 'accounts/login.html',
			'extra_context': {'title': _('Login')},
			'authentication_form': EmailAuthenticationForm
		},
		name='login'
	),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
	url(r'^singup/$', views.singup, name='singup'),

	url(
		r'^password_change/$',
		'django.contrib.auth.views.password_change',
		{
			'template_name': 'accounts/password_change.html',
			'extra_context': {'title': _('Change password')}
		},
	name='password_change'
	),

	url(
		r'^password_change/done/$',
		'django.contrib.auth.views.password_change_done',
		{
			'template_name': 'accounts/password_change_done.html',
			'extra_context': {'title': _('Change password')}
		},
		name='password_change_done'
	),

	url(
		r'^password_reset/$',
		'django.contrib.auth.views.password_reset',
		{'template_name': 'accounts/password_reset.html'},
		name='password_reset'
	),

	url(
		r'^password_reset/done/$',
		'django.contrib.auth.views.password_reset_done',
		{'template_name': 'accounts/password_reset_done.html'},
		name='password_reset_done'
	),

	url(
		r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		'django.contrib.auth.views.password_reset_confirm',
		{'template_name': 'accounts/password_reset_confirm.html'},
		name='password_reset_confirm'
	),

	url(
		r'^reset/done/$',
		'django.contrib.auth.views.password_reset_complete',
		{'template_name': 'accounts/password_reset_complete.html'},
		name='password_reset_complete'
	),


	url(r'^profile/$', views.profile, name='profile'),
	url(r'^profile/edit/$', views.edit, name='accounts_edit'),

	url(r'^bucket/$', views.bucket, name='bucket'),

	# url(r'^bucket/sync/$', views.bucket_sync, name='bucket_sync'),
	# url(r'^bucket/clear/$', views.bucket_clear, name='bucket_clear'),

	url(r'^bucket/update/$', views.bucket_update, name='bucket_update'),


	url(r'^order/$', views.order, name='order'),

	url(r'^orders_list$', views.orders_list, name='orders_list'),
	# url(r'^orders_update$', views.orders_update, name='orders_update'),
	url(r'^orders_confirm$', views.orders_confirm, name='orders_confirm'),
]
