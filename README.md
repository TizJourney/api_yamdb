# api_yamdb
Проект имитирует api для работы с социальной сетью
## Функциональность
* Добавление и получение списка постов
* Добавление и получение списка комментариев к посту
* Добавление и получение списка подписчиков на посты
* TODO: ..

## Установка

### Виртуальное окружение
* Ставим виртуальное окружение: `python -m venv venv`
* Запускаем виртуальное окружение: (windows) `source venv/Scripts/activate` или (mac/linux) `source venv/bin/activate`

### Сборка окружения
* Продакшен сборка:  `pip install -r requirements.txt`
* Для разработки рекомендутеся dev-сборка: `pip install -r requirements_dev.txt`

### Настройка базы данных
* Если не используется заранее сохранённая база, то требуется инициализировать пустую базу: `python manage.py migrate` 

### Запуск
* Запуск локального сервера `python manage.py runserver`

### Заведение супер пользователя
* Далее нужно завести супер-пользователя `python manage.py createsuperuser`
* Супер-пользователь может создавать контент для базы данных через панель админа: `<адрес виртуального сервера>\admin`

### Залить данные из текстовых файлов в базу данных
* Из корневой директории запустить: `python ./script/csw_sqlite3.py`

## Работа с API
### Документация 
* Документацию для api можно найти по адресу: `<адрес виртуального сервера>\redoc`

### Авторизация
* В проекте используется [Signature JWT](https://jwt.io/introduction/)
* Пример запроса на авторизацию для виртуального сервера `http://127.0.0.1:8000`:
```
curl --location --request POST 'http://127.0.0.1:8000/api/v1/token/' \
--form 'username=логин' \
--form 'password=пароль'
```
* Пример запроса для создания поста API с использованием токена авторизации:
```
curl --location --request POST 'http://127.0.0.1:8000/api/v1/posts/1/comments/' \
--header 'Authorization: Bearer <тут access токен>' \
--form 'text=Какой-то текст поста'
```


### Если возникнет ошибка ```migration admin.0001_initial```

* Закомментировать в settings.py в `INSTALLED_APPS` строчку `api` и `AUTH_USER_MODEL = 'api.YamDBUser'`

* Обнулить миграции пользователей 
```
python manage.py migrate admin zero
python manage.py migrate auth zero
python manage.py migrate contenttypes zero
python manage.py migrate sessions zero
```
* Расскомменитировать строчки выше
* Сделать миграцию: `python manage.py migrate`

### Как посмотреть схемы и название таблиц в базе данных
* Можно использовать команду `python manage.py inspectdb`