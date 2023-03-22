import string
import random

from django.core.mail import send_mail
from rest_framework import views, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Title
from .serializers import (
    SingUpSerializer,
    User,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    MyObtainTokenSerializer,
)


class ObtainTokenView(views.APIView):
    """Генерирет Acceess_token при получении validation_code и username"""

    serializer_class = MyObtainTokenSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
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
