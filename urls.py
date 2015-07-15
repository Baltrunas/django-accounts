from django.conf.urls import url

from .views import singup
from .views import bucket
from .views import bucket_add
from .views import bucket_delete
from .views import bucket_edit
from .views import bucket_sync
from .views import bucket_clear

from .views import profile
from .views import edit

from .views import order

from .views import change_password


urlpatterns = [
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
	url(r'^singup/$', singup, name='singup'),

	url(r'^profile/$', profile, name='profile'),
	url(r'^profile/edit/$', edit, name='accounts_edit'),

	url(r'^bucket/delete/$', bucket_delete, name='bucket_delete'),
	url(r'^bucket/add/$', bucket_add, name='bucket_add'),
	url(r'^bucket/edit/$', bucket_edit, name='bucket_edit'),
	url(r'^bucket/sync/$', bucket_sync, name='bucket_sync'),
	url(r'^bucket/clear/$', bucket_clear, name='bucket_clear'),
	url(r'^bucket/$', bucket, name='bucket'),
	url(r'^order/$', order, name='order'),

	url(r'^change_password/$', change_password, name="change_password"),
]
