from rest_framework import serializers

from reviews.models import Category, Genre, Title


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

    # genre = GenreSerializer(read_only=True, many=True)
    # category = CategorySerializer(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title
