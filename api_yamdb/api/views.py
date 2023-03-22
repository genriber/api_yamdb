import string
import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (
    SingUpSerializer,
    User,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
)

from .permissions import (
    IsAuthorOrReadOnly,
    IsAdminOrReadOnly,
    IsAdminOrModeratorOrReadOnly,
)
from .filters import TitleFilter


class SingUpView(views.APIView):
    """Генерирует verification_code и отправляет на email пользователя"""

    serializer_class = SingUpSerializer
    permission_classes = [
        AllowAny,
    ]

    def genereate_confirmation_code(self):
        length = 6
        password = "".join(random.choices(string.ascii_letters, k=length))
        return password

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            username = serializer.data.get("username")
            password = self.genereate_confirmation_code()
            send_mail(
                "Yamdb registration",
                f"confirmation_code : {password}",
                "from@example.com",
                [{email}],
                fail_silently=False,
            )
            user = User.objects.update_or_create(
                email=email, username=username, password=password
            )

            return Response(
                SingUpSerializer(user).data, status=status.HTTP_200_OK
            )

        return Response(
            serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
        )


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Вьюсет категорий
    Права доступа: Доступно без токена
    """

    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "slug"]

    @action(
        detail=False,
        methods=["delete"],
        url_path=r"(?P<slug>\w+)",
        lookup_field="slug",
        url_name="category_slug",
    )
    def get_category_for_delete(self, request, slug):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, slug=slug)
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    """
    Вьюсет жанров
    Права доступа: Доступно без токена
    """

    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "slug"]

    @action(
        detail=False,
        methods=["delete"],
        url_path=r"(?P<slug>\w+)",
        lookup_field="slug",
        url_name="genre_slug",
    )
    def get_genre_for_delete(self, request, slug):
        queryset = Genre.objects.all()
        genre = get_object_or_404(queryset, slug=slug)
        serializer = GenreSerializer(genre)
        genre.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет произведений
    Права доступа: Доступно без токена
    """

    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет всех отзывов
    Права доступа: Доступно без токена
    """

    permission_classes = [IsAdminOrModeratorOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = LimitOffsetPagination


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет всех всех комментариев к отзыву по id
    Права доступа: Доступно без токена
    """

    permission_classes = [IsAdminOrModeratorOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = LimitOffsetPagination
