# API_YAMDB

![1679584208063](image/README/1679584208063.png)

### **Проект выполнен в рамках обучения в YandexPracticum.**

REST Like Backend проекта сбора отзывов выполнен согласно представленной в ТЗ документации, оформленой по стандартам OpenAPI в виде [ReDoc](https://github.com/genriber/api_yamdb/blob/master/api_yamdb/static/redoc.yaml) веб станицы. Для соблюдения принципов DRY и SOLID в разработке используются Rest_framework ViewSet, Generics, Mixins. Для авторизации применяются JWT токены.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/genriber/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3.9 -m venv env
```

* Если у вас Linux/macOS

  ```
  source env/bin/activate
  ```
* Если у вас windows

  ```
  source env/scripts/activate
  ```

```
python3.9 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```


## Эндпойнты и примеры запросов
### Эндпойнт для получения списка всех произведений
#### Запрос:
```http://127.0.0.1:8000/api/v1/titles/?limit=1```
#### Ответ:
```
{
    "count": 33,
    "next": "http://127.0.0.1:8000/api/v1/titles/?limit=1&offset=1",
    "previous": null,
    "results": [
        {
            "id": 3,
            "category": {
                "name": "Фильм",
                "slug": "movie"
            },
            "genre": [
                {
                    "name": "Драма",
                    "slug": "drama"
                }
            ],
            "rating": 8,
            "name": "12 разгневанных мужчин",
            "year": 1957,
            "description": ""
        }
    ]
}
```
### Эндпойнт для получения списка всех отзывов к произведению
#### Запрос:
```
http://127.0.0.1:8000/api/v1/titles/1/reviews/?limit=1
```
#### Ответ:
```
{
    "count": 29,
    "next": "http://127.0.0.1:8000/api/v1/titles/1/reviews/?limit=1&offset=1",
    "previous": null,
    "results": [
        {
            "id": 1,
            "text": "Ставлю десять звёзд!\n...Эти голоса были чище и светлее тех, о которых мечтали в этом сером, убогом месте. Как будто две птички влетели и своими голосами развеяли стены наших клеток, и на короткий миг каждый человек в Шоушенке почувствовал себя свободным.",
            "author": "bingobongo",
            "score": 10,
            "pub_date": "2023-03-22T17:03:31.479577Z"
        }
    ]
}
```

## Авторы

[Alexey Kargaev](https://github.com/genriber), [Andrey Shchiptsov](https://github.com/Bigbrotherx) и [Arseniiy Kapshtyk](https://github.com/Kapshtak).
