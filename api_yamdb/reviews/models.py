from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Review(models.Model):
    title = models.ForeignKey(
        "Title",
        verbose_name="Оцениваемое произведение",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор отзыва",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField(verbose_name="Текст отзыва", null=False)
    score = models.IntegerField(
        verbose_name="Оценка автора отзыва",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации отзыва", auto_now_add=True
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_author_title_pair"
            )
        ]

    def __str__(self):
        return (
            f"Отзыв {self.author.username} на произведение {self.title.name}"
        )

    def get_mean_score(self, title_id):
        title = get_object_or_404(Title, pk=title_id)
        try:
            return round(
                Review.objects.filter(title=title).aggregate(
                    models.Avg("score")
                )
            )
        except:
            return 0


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        "Review", on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации комментария", auto_now_add=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        constraints = [
            models.CheckConstraint(
                check=~models.Q(author=models.F("review__author")),
                name="sefl_commenting_check",
            )
        ]

    def __str__(self):
        return (
            f"Комментарий {self.author.username} на "
            f"отзыв {self.review.author.name}"
        )
