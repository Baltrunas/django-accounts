from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
	name = 'apps.accounts'
	label = 'accounts'
	verbose_name = _('Accounts')

	def ready(self):
		import signals

