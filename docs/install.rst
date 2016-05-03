Установка
=========

* Скопируйте или склонируйте проект в папку ``accounts`` в пределах области видимости
* Добавьте ``url(r'^', include('accounts.urls')),`` в файл urls.py
* Добавьте ``'accounts',`` в INSTALLED_APPS файла settings.py
* Синхронизируйте базу данных командой ``manage.py migrate``
* Соберите статику ``manage.py collectstatic``
* При необходимости подключите стили и скрипты модуля (вставив нижеприведённые код между тегами ``<head></head>``)


.. code-block:: html

    {% load staticfiles %}
    <link rel="stylesheet" href="{% static "accounts/css/accounts.css" %}">
    <script src="{% static "accounts/js/accounts.js" %}" type="text/javascript"></script>
