Api
===

Проверка авторизации
---------------------

**/api/json/check/**

POST

    | username - логин для авторизации (requered)
    | password - пароль для авторизации (requered)

Варианты ответа:

Всё ок:

.. code-block:: javascript

    {"auth": true}

Неправильный логин или пароль:

.. code-block:: javascript

    {"auth": false}



Список заказов
--------------
**/api/json/order/list/$status/**

$status - типы заказов может быть: 
    | new - новые
    | my - мои текушие заявки
    | history - обработаенные и отмененные

POST

    | username - логин для авторизации (requered)
    | password - пароль для авторизации (requered)

Варианты ответа:

Всё ок:

.. code-block:: javascript

    {
        "orders": [
            {
                "status": "accept",
                "phone": "+996500000000",
                "name": "Vasya Pupkin",
                "address": "5mk 12h 71kv",
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

Неправильный логин или пароль:

.. code-block:: javascript

    {"auth": false}


"auth": true - говорит о том что аутентификация прошла успешно (иначе false и не будет списка)

orders - сам список

status - бывает (в разных списках набор статусов ограничен):

    | new - новая не принятая заявка
    | accept - принятая заявка
    | processed - в процессе
    | paid - оплаченно
    | success - успешно завершена
    | canceled - отмененная
    | accounting - отправлено ли в 1с

accounting - отправлено ли в 1с



Новая заявка
------------
**/api/json/order/accept/$id/**

$id - id заказа

POST

    | username - логин для авторизации (requered)
    | password - пароль для авторизации (requered)

Варианты ответа:

 Если заявка успешна принята:

 .. code-block:: javascript

        {
            "status": "accept",
            "auth": true,
            "acceptor": "admin"
        }

 Неправильный логин или пароль:

 .. code-block:: javascript

         {"auth": false}


Отправка в 1с (только если в настройках сайта выставлена галочка отправки в бухгалтерию)
----------------------------------------------------------------------------------------
**/api/json/order/accounting/$id/**

$id - id заказа

POST

    | username - логин для авторизации (requered)
    | password - пароль для авторизации (requered)
Варианты ответа:

Если успешно:

.. code-block:: javascript

    {
        "status": "ok",
        "auth": true
    }

Если заявка не найдена:

.. code-block:: javascript

    {
        "status": "Error, order not found!",
        "auth": true
    }

Неправильный логин или пароль:

.. code-block:: javascript

    {"auth": false}


Изменение статуса заказа
------------------------
**/api/json/order/status/$status/$id/**

$status - статусы заказа могут быть: 

    | processed - обработанный
    | paid - оплаченный
    | success - успешно завершенный
    | canceled - отмененный

$id - id заказа

POST

    | username - логин для авторизации (requered)
    | password - пароль для авторизации (requered)

Варианты ответа:

Если успешно:

.. code-block:: javascript

    {
        "status": "ok",
        "auth": true
    }

Если заявка не найдена:

.. code-block:: django

    Order matching query does not exist.

Неправильный логин или пароль

.. code-block:: javascript

    {"auth": false}


Редактирование заявки
---------------------
**/api/json/order/update/$id/**

$id - id заказа

POST

    | username - логин для авторизации (requered)
    | password - пароль для авторизации (requered)
    | name - Имя заказчика (requered)
    | email - email заказчика
    | address - address заказчика (requered)
    | phone - phone заказчика (requered)
    | comment - комментарий заказчика
    | payment_method - способ оплаты заказа (requered)

Варианты ответа:

Если успешно:

.. code-block:: javascript

    {
        "status": true,
        "auth": true
    }

Если форма не валидна:

.. code-block:: javascript

    {
        "status": false,
        "errors": {"payment_method": ["Обязательное поле."], "phone": ["Обязательное поле."], "name": ["Обязательное поле."], "address": ["Обязательное поле."]},
        "auth": true
    }

Неправильный логин или пароль

.. code-block:: javascript

    {"auth": false}


Добавление товара к заказу
------------------------
**/api/json/order/item/add/$id/**

$id - id заказа

POST

    | username - логин для авторизации (requered)
    | password - пароль для авторизации (requered)
    | discount_price - цена товара со скидкой
    | count - количество товара

Варианты ответа:

Если успешно:

.. code-block:: javascript

    {
        "status": true,
        "auth": true
    }

Если форма не валидна:

.. code-block:: javascript

    {
        "status": false,
        "auth": true
    }

Неправильный логин или пароль

.. code-block:: javascript

    {"auth": false}


Удаление темы заказа
------------------------
**/api/json/order/item/delete/$id/**

$id - id тема заказа

POST
    | username - логин для авторизации (requered)
    | password - пароль для авторизации (requered)

Варианты ответа:

Если успешно:

.. code-block:: javascript

    {
        "status": true,
        "auth": true
    }

Неправильный логин или пароль:

.. code-block:: javascript

    {"auth": false}
