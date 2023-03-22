from rest_framework import serializers

from reviews.models import User, Category, Genre, Title, Review, Comment


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

    class Meta:
        fields = "__all__"
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = "__all__"
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = "__all__"
        model = Comment
