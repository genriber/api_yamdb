from django.contrib.auth import authenticate
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User, Category, Genre, Title, models


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
        fields = "__all__"
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров
    """

    class Meta:
        fields = "__all__"
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров
    """

    class Meta:
        fields = "__all__"
        model = Title
