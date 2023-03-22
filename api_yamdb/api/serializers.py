from django.contrib.auth import authenticate
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User, Category, Genre, Title, models


class MyObtainTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(
        max_length=150, min_length=6, write_only=True, source="password"
    )

    class Meta:
        model = User
        fields = ("username", "confirmation_code")
        extra_kwargs = {
            "username": {"validators": [UnicodeUsernameValidator()]},
        }

    def validate(self, data):
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
        try:
            get_object_or_404(
                User, email=data["email"], username=data["username"]
            )
        except Http404:
            queryset = User.objects.filter(
                models.Q(email=data["email"])
                | models.Q(username=data["username"])
            )
            if queryset.exists():
                raise serializers.ValidationError(
                    "Имя и email должны быть уникальными!"
                )

        return data


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
