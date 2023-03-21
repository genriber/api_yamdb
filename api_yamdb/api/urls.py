from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import SingUpView

app_name = "api"


urlpatterns = [
    path("v1/auth/signup/", SingUpView.as_view(), name="singup"),
    path(
        "v1/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_access",
    ),
]
