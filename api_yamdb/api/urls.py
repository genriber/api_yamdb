from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    SingUpView,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ObtainTokenView,
    UsersListView,
)

app_name = "api"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"titles", TitleViewSet)
router.register(r"users", UsersListView)

urlpatterns = [
    path("v1/auth/signup/", SingUpView.as_view(), name="singup"),
    path(
        "v1/auth/token/",
        ObtainTokenView.as_view(),
        name="token_obtain_access",
    ),
    path("v1/", include(router.urls)),
]
