Api
===

Проверка правильности
---------------------
**/api/json/check/**
POST
	login - логин для авторизации
	password - пароль для авторизации
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
	login - логин для авторизации
	password - пароль для авторизации
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
	| orders - сам список
status - бывает (в разных списках набор статусов ограничен):
	| new - новая не принятая заявка
	| accept - принятая заявка
	| processed - в процессе
	| paid - оплаченно
	| success - успешно завершена canceled - отмененная
	| accounting - отправлено ли в 1с
accounting - отправлено ли в 1с

