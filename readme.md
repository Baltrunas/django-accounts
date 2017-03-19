'apps.accounts',

'apps.accounts.context_processors.bucket',

AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = ('apps.accounts.auth.EmailOrUsernameModelBackend',)


ACCOUNTS_PAYMENTS = [
    ('cash', 'Cash'),
    ('robox', 'Robokassa'),
    ('mobilnik', 'Mobilnik'),
    ('demirbank', 'DemirBank'),
]

DEFAULT_VALUTE = 'usd'


---	
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

SOCIAL_AUTH_USER_MODEL = 'accounts.User'


SMS_TO = ''

разобраться с apps.py и __init__.py





bucket.html
	оформить
	классы
	стили
	добавление с релейтедов аяксом

юид в форму или в модель

список релейтов аяксом
почистить

accounts.js полностью обработка от аякса, некаких псевдо смен цен
accounts.css полностью забить стили


мультивалюты
платежи

написать новый ридми




каталог
	проверить модели
	проверить админку
	проверить формы
	обновить ридми
	проверить урл
	проверить апи
	проверить вьюхи
	проверить и обновить шаблоны
	шаблонные теги
	стили
	статика
	переводы
	команды


# order_status
	# Новый
	# Принят
	# Готов
	# Выполнен
	# Отменён


# delivery_status
	# НА ОФОРМЛЕНИИ
	# ДОСТАВКА
	# ГОТОВ К ВЫДАЧЕ
	# Доставелен
	# Отменён
	# Возврат



заказы
	полное имя
	емейл
	адресс
	телефон
	цена
	ид заказа




seo


