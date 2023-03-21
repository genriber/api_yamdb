from rest_framework import serializers

from reviews.models import User, Category, Genre, Title


class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "email",
            "username",
        )
        model = User

    def create(self, validated_data):
        user = User.objects.update_or_create(**validated_data)
        return user


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
