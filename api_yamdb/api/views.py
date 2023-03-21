import string
import random

from django.core.mail import send_mail
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import SingUpSerializer, User


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
