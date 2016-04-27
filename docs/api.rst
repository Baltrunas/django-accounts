Api
===

Проверка правильности
---------------------
**/api/json/check/**
POST
	| login - логин для авторизации
	| password - пароль для авторизации
Варианты ответа:
	``{"auth": true}``
	Всё ок
	``{"auth": false}``
	Неправильный логин или пароль


Список заказов
---------------------
**/api/json/order/list/$status/**
$status - типы заказов может быть: 
	| new - новые
	| my - мои текушие заявки
	| history - обработаенные и отмененные
POST
	| login - логин для авторизации
	| password - пароль для авторизации
Варианты ответа:

.. code-block:: html

	{
		"orders": [
			{
				"status": "accept",
				"phone": "+996555338874",
				"name": "Stanislav Baltrunas",
				"address": "7mk 22h 74kv",
				"order_items": [
					{
						"count": 8,
						"price": "8.0000",
						"id": 4,
						"name": "Snowboard"
					},
				],
				"accounting": false,
				"created_at": "2016-02-23 16:58:09",
				"total": "90.0000",
				"id": 2,
				"comment": ""
			}
		]
	}

Всё ок

	``{"auth": false}``
Неправильный логин или пароль

"auth": true - говорит о том что аутентификация прошла успешно (иначе false и не будет списка)
orders - сам список
status - бывает (в разных списках набор статусов ограничен):
	| new - новая не принятая заявка
	| accept - принятая заявка
	| processed - в процессе
	| paid - оплаченно
	| success - успешно завершена canceled - отмененная
	| accounting - отправлено ли в 1с
accounting - отправлено ли в 1с



Новая заявка
---------------------
**/api/json/order/accept/$id/**
$id - id заказа
POST
	| login - логин для авторизации
	| password - пароль для авторизации
Варианты ответа:
	Если заявка успешна принята:
	.. code-block:: html
		{
			"status": "accept",
			"auth": true,
			"acceptor": "admin"
		}

	Неправильный логин или пароль:
		``{"auth": false}``


Отправка в 1с (только если в настройках сайта выставлена галочка отправки в бухгалтерию)
---------------------
**/api/json/order/accounting/$id/**
POST
	| login - логин для авторизации
	| password - пароль для авторизации
Варианты ответа:
	Если успешно:
	.. code-block:: html
		{
			"status": "ok",
			"auth": true
		}
	Если заявка не найдена:
	.. code-block:: html
		{
			"status": "Error, order not found!",
			"auth": true
		}
	Неправильный логин или пароль
		``{"auth": false}``


Изменение статуса заказа
------------------------
**/api/json/order/status/$status/$id/**
$status - статусы (processed, paid, success, canceled)
$id - id заказа
POST
	| login - логин для авторизации
	| password - пароль для авторизации
Варианты ответа:
	Если успешно:
	.. code-block:: html
		{
			"status": "ok",
			"auth": true
		}
	Если заявка не найдена:
		``Order matching query does not exist.``
	Неправильный логин или пароль
		``{"auth": false}``


Редактирование заявки
------------------------
**/api/json/order/update/$id/**
$id - id заказа
POST
 	| login - логин для авторизации
	| password - пароль для авторизации
	| name = name заказа
	| email - email заказа
	| address - address заказа
	| phone - phone заказа
	| comment - comment заказа
	| payment_method - payment_method заказа
Варианты ответа:
	Если успешно:
	.. code-block:: html
		{
			"status": true,
			"auth": true
		}
	Если форма не валидна:
	.. code-block:: html
		{
			"status": false,
			"errors": {"payment_method": ["Обязательное поле."], "phone": ["Обязательное поле."], "name": ["Обязательное поле."], "address": ["Обязательное поле."]},
			"auth": true
		}
	Неправильный логин или пароль
		``{"auth": false}``


Добавление темы заказа
------------------------
**/api/json/order/item/add/$id/**
$id - id темы заказа
POST
	| login - логин для авторизации
	| password - пароль для авторизации
	| discount_price - цена
	| count - количество
Варианты ответа:
	Если успешно:
	.. code-block:: html
		{
			"status": true,
			"auth": true
		}
	Если форма не валидна:
	.. code-block:: html
		{
			"status": false,
			"auth": true
		}
	Неправильный логин или пароль
		``{"auth": false}``


Удаление темы заказа
------------------------
**/api/json/order/item/delete/$id/**
$id - id тема заказа
POST
	login - логин для авторизации
	password - пароль для авторизации
Варианты ответа:
	Если успешно:
	.. code-block:: html
		{
			"status": true,
			"auth": true
		}
	Неправильный логин или пароль
		``{"auth": false}``
