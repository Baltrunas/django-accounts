from django.conf import settings

payments = [payment[0] for payment in settings.ACCOUNTS_PAYMENTS]

if 'cash' in payments:
	from . import cash
if 'mobilnik' in payments:
	from . import mobilnik
if 'robox' in payments:
	from . import robox
if 'demirbank' in payments:
	from . import demirbank
