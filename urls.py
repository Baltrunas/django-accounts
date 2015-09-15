from django.conf.urls import url, include

from django.utils.translation import ugettext_lazy as _

from . import views


urlpatterns = [
	# url('^', include('django.contrib.auth.urls')),
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
	url(r'^change_password/$', views.change_password, name='change_password'),

	url(r'^profile/$', views.profile, name='profile'),
	url(r'^profile/edit/$', views.edit, name='accounts_edit'),

	url(r'^bucket/$', views.bucket, name='bucket'),

	# url(r'^bucket/sync/$', views.bucket_sync, name='bucket_sync'),
	# url(r'^bucket/clear/$', views.bucket_clear, name='bucket_clear'),

	url(r'^bucket/update/$', views.bucket_update, name='bucket_update'),


	url(r'^order/$', views.order, name='order'),

]
