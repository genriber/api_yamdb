from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Genre, Title
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)


class CategoryViewSet(viewsets.GenericViewSet):
    """Вьюсет категорий. Права доступа: Доступно без токена"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.GenericViewSet):
    """Вьюсет жанров. Права доступа: Доступно без токена"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.GenericViewSet):
    """Вьюсет произведений. Права доступа: Доступно без токена"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
