import random
import string

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import filters, generics, status, views, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from reviews.models import Category, Comment, Genre, Review, Title, models
from .filters import TitleFilter
from .permissions import (
    AdminOnly,
    IsAdminOrReadOnly,
    IsAdOrModOrAuthorOrReadOnly,
)
from .serializers import (
    AdminCreateSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    MyObtainTokenSerializer,
    ProfileSerializer,
    ReviewSerializer,
    SingUpSerializer,
    TitleSerializer,
    TitleReadOnlySerializer,
    User,
)
from .permissions import (
    AdminOnly,
    IsAdminOrReadOnly,
    AdminOnly,
    IsAdOrModOrAuthorOrReadOnly,
)
from .filters import TitleFilter
from .mixins import RestrictedActionsViewSet


class ObtainTokenView(views.APIView):
    """Генерирет Acceess_token при получении validation_code и username"""

    serializer_class = MyObtainTokenSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        """Обработка post запроса на получение токена."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"token": serializer.validated_data.get("access")},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class SingUpView(views.APIView):
    """Генерирует verification_code и отправляет на email пользователя"""

    serializer_class = SingUpSerializer
    permission_classes = [
        AllowAny,
    ]

    def genereate_confirmation_code(self):
        """Генерация сучайного confirmation_code"""
        length = 6
        code = "".join(random.choices(string.ascii_letters, k=length))
        return code

    def post(self, request, format=None):
        """Обработка POST запроса"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            username = serializer.data.get("username")
            if username == "me":
                raise ValidationError("Недопустимое имя!")
            password = self.genereate_confirmation_code()
            send_mail(
                "Yamdb registration",
                f"confirmation_code : {password}",
                "from@example.com",
                (f"{email}",),
                fail_silently=False,
            )
            user, _ = User.objects.update_or_create(
                email=email, username=username
            )
            user.set_password(password)
            user.save()

            return Response(
                SingUpSerializer(user).data, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersListViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователей доступен только админам"""

    permission_classes = [
        AdminOnly,
    ]
    queryset = User.objects.all()
    serializer_class = AdminCreateSerializer
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    pagination_class = LimitOffsetPagination


class UserMeApiView(generics.RetrieveAPIView, generics.UpdateAPIView):
    """Вьюсет профиля пользователя"""

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Получения объекта из запроса"""
        return self.request.user


class CategoryViewSet(RestrictedActionsViewSet):
    """
    Вьюсет категорий.
    Права доступа:
        GET: Доступно без токена
        POST/etc: Админ
    """

    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "slug"]
    lookup_field = "slug"


class GenreViewSet(RestrictedActionsViewSet):
    """
    Вьюсет категорий.
    Права доступа:
        GET: Доступно без токена
        POST/etc: Админ
    """

    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "slug"]
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет категорий.
    Права доступа:
        GET: Доступно без токена
        POST/etc: Админ
    Присутствует кастомная фильтрация:
        Возможен поиск по полю genre с параметром slug.
    """

    permission_classes = [IsAdminOrReadOnly]
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]
    queryset = Title.objects.all().annotate(
        average_rating=models.Avg("reviews__score")
    )
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TitleReadOnlySerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов."""

    permission_classes = [IsAdOrModOrAuthorOrReadOnly]
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        get_object_or_404(Title, pk=title_id)
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментов."""

    permission_classes = [IsAdOrModOrAuthorOrReadOnly]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        get_object_or_404(Title, pk=title_id)
        get_object_or_404(Review, pk=review_id)
        return Comment.objects.filter(review=review_id)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
