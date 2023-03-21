import string
import random

from django.core.mail import send_mail
from rest_framework import views, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from reviews.models import Category, Comment, Genre, Review, Title
from .serializers import (
    SingUpSerializer,
    User,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
)


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
    """Вьюсет категорий. Права доступа: Доступно без токена"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет жанров. Права доступа: Доступно без токена"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений. Права доступа: Доступно без токена"""

    permission_classes = [
        AllowAny,
    ]
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов."""

    permission_classes = [
        AllowAny,
    ]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = LimitOffsetPagination
