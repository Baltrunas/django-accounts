from django.conf import settings

if 'cash' in settings.ACCOUNTS_PAYMENTS:
	from . import cash
if 'mobilnik' in settings.ACCOUNTS_PAYMENTS:
	from . import mobilnik
if 'robox' in settings.ACCOUNTS_PAYMENTS:
	from . import robox
if 'demirbank' in settings.ACCOUNTS_PAYMENTS:
	from . import demirbank
