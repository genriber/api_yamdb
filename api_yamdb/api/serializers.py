from rest_framework import serializers

from reviews.models import User, Category, Comment, Genre, Review, Title


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


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор отзывов
    """

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review
