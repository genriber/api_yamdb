import string
import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, status, viewsets, filters, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (
    CommentSerializer,
    SingUpSerializer,
    User,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    MyObtainTokenSerializer,
    AdminCreateSerializer,
    ProfileSerializer,
)
from .permissions import (
    AdminOnly,
    IsAuthorOrReadOnly,
    IsAdminOrReadOnly,
    AdminOnly,
    IsAdminOrModeratorOrReadOnly,
    IsAdOrModOrAuthorOrReadOnly,
)
from .filters import TitleFilter


class ObtainTokenView(views.APIView):
    """Генерирет Acceess_token при получении validation_code и username"""

    serializer_class = MyObtainTokenSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        """Генерация сучайного confirmation_code"""
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
        return self.request.user


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
    """Вьюсет отзывов."""

    # permission_classes = [IsAdminOrModeratorOrReadOnly, IsAuthorOrReadOnly]
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
