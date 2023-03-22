from django.contrib.auth import authenticate
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import (
    Comment,
    User,
    Category,
    Genre,
    Review,
    Title,
    models,
)


def validate_uniqe_user_data(data):
    queryset = User.objects.filter(
        models.Q(email=data["email"]) | models.Q(username=data["username"])
    )
    if queryset.exists():
        raise serializers.ValidationError(
            "Имя и email должны быть уникальными!"
        )


class MyObtainTokenSerializer(serializers.ModelSerializer):
    """Сериализатор получения токена для зарегистрированного пользователя."""

    confirmation_code = serializers.CharField(
        max_length=150, min_length=4, write_only=True, source="password"
    )

    class Meta:
        model = User
        fields = ("username", "confirmation_code")
        extra_kwargs = {
            "username": {"validators": [UnicodeUsernameValidator()]},
        }

    def validate(self, data):
        """Валидатор для 'username' и 'confirmation_code'."""
        user = get_object_or_404(User, username=data["username"])
        authenticate_kwargs = {
            "username": user.username,
            "password": data["password"],
        }
        user = authenticate(**authenticate_kwargs)
        if user is None:
            raise exceptions.ValidationError("Неверный пароль!")
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
        }


class SingUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации через email"""

    class Meta:
        fields = (
            "email",
            "username",
        )
        extra_kwargs = {
            "email": {"required": True},
            "username": {
                "required": True,
                "validators": [UnicodeUsernameValidator()],
            },
        }
        model = User

    def create(self, validated_data):
        """Если пользователь уже создан взять существующего"""
        return User.objects.get_or_create(**validated_data)

    def validate(self, data):
        """
        Валидация в 2 этапа:
         1. Ищем пользователя в базе если находим валидация успешна
         2. Если пользователя нет проверяем что username и email уникальны
        """
        try:
            get_object_or_404(
                User, email=data["email"], username=data["username"]
            )
        except Http404:
            validate_uniqe_user_data(data)
        return data


class AdminCreateSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователей админом"""

    class Meta:
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        extra_kwargs = {
            "email": {"required": True},
            "username": {
                "required": True,
                "validators": [UnicodeUsernameValidator()],
            },
        }
        model = User

    def create(self, validated_data):
        if validated_data.get("role") is None:
            validated_data["role"] = "user"
        return super().create(validated_data)

    def validate(self, data):
        validate_uniqe_user_data(data)

        return super().validate(data)


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий
    """

    class Meta:
        exclude = ["id"]
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров
    """

    class Meta:
        exclude = ["id"]
        model = Genre


class TitleCategory(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class TitleGenre(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров
    """

    category = TitleCategory(
        slug_field="slug",
        queryset=Category.objects.all(),
    )
    genre = TitleGenre(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = "__all__"
        model = Title

    def get_rating(self, obj):
        return Review.get_mean_score(obj.pk)


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор отзывов
    """

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
        default=serializers.CurrentUserDefault(),
        read_only=False,
        required=False,
    )
    title = serializers.HiddenField(default=None)

    def validate_title(self, value):
        title_id = self.context["view"].kwargs["title_id"]
        return get_object_or_404(Title, pk=title_id)

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date", "title")
        model = Review
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=("author", "title"),
                message="Вы не можете дважды комментировать одно произведение",
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор комментариев
    """

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
        read_only=False,
        required=False,
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
