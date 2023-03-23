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
