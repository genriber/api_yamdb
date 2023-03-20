from datetime import date
from django.core.validators import MaxValueValidator, validate_slug
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """
    Модель для категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    Одно произведение может быть привязано только к одной категории.
    """

    name = models.CharField(
        "Название категории",
        max_length=256,
    )
    slug = models.SlugField(
        "Слаг категории",
        unique=True,
        max_length=50,
        validators=[validate_slug],
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Модель для жанров произведений.
    Одно произведение может быть привязано к нескольким жанрам.
    """

    name = models.CharField(
        "Название жанра",
        max_length=256,
    )
    slug = models.SlugField(
        "Слаг жанра", unique=True, max_length=50, validators=[validate_slug]
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы
    (определённый фильм, книга или песенка).
    """

    name = models.CharField(
        "Название произведения",
        max_length=256,
    )
    year = models.PositiveIntegerField(
        "Год выпуска произведения",
        validators=[
            MaxValueValidator(
                date.today().year,
                message="Нельзя добавить произведения из будущего",
            ),
        ],
    )
    description = models.TextField(
        "Описание",
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        null=True,
        related_name="titles",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="titles",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name
