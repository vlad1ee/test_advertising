# Test Advertising
***
* Установить зависимости
```
pip install requirements.txt
```
* Запустить миграции
```
python manage.py makemigrations
```
* Применить миграции
```
python manage.py migrate
```
* Создать суперпользователя и объект модели Category

### URL проекта
* api/v1/ - основной, к нему добавляются остальные
---
  * auth/sign-up - POST -регистрация пользователя (email, username, password)
  * auth/sign-in - POST -логин пользователя (email, password) и получение access и refresh токенов
---
  * advertising/ - POST - Создание объявления
  * advertising/ - GET - Получение объявления (query_params - author_id для фильтрации объявлений по автору)
  * change-status/ - POST - Изменение статуса объявлений (Оплачено/Отказ).