from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


USER_ROLE_CHOISES = (
    ("user", "Авторизованный пользователь"),
    ("moderator", "Модератор"),
    ("admin", "Администратор"),
)


class User(AbstractUser):
    """Кастомный класс модели User"""

    bio = models.TextField(
        "Биография", blank=True, help_text="Расскажите о себе"
    )
    role = models.CharField(
        "Пользовательская роль",
        max_length=10,
        blank=True,
        choices=USER_ROLE_CHOISES,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["email", "username"],
                name="unique_pair",
            ),
        ]
        ordering = ["username"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return f"Пользователь {self.username} - {self.role}"
