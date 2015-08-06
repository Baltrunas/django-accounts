from django.conf.urls import url

from django.utils.translation import ugettext_lazy as _

from . import views


urlpatterns = [
	url(
		r'^login/$',
		'django.contrib.auth.views.login',
		{
			'template_name': 'accounts/login.html',
			'extra_context': {'title': _('Login')}
		},
		name='login'
	),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
	url(r'^singup/$', views.singup, name='singup'),

	url(r'^profile/$', views.profile, name='profile'),
	url(r'^profile/edit/$', views.edit, name='accounts_edit'),

	url(r'^bucket/update/$', views.bucket_update, name='bucket_update'),

	url(r'^bucket/delete/$', views.bucket_delete, name='bucket_delete'),
	url(r'^bucket/add/$', views.bucket_add, name='bucket_add'),
	url(r'^bucket/edit/$', views.bucket_edit, name='bucket_edit'),
	url(r'^bucket/sync/$', views.bucket_sync, name='bucket_sync'),
	url(r'^bucket/clear/$', views.bucket_clear, name='bucket_clear'),
	url(r'^bucket/$', views.bucket, name='bucket'),
	url(r'^order/$', views.order, name='order'),

	url(r'^change_password/$', views.change_password, name="change_password"),
]
