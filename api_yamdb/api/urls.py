from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    SingUpView,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

app_name = "api"

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register("titles", TitleViewSet)
router.register(
    r"titles/(?P<title_id>[\d.]+)/reviews",
    ReviewViewSet,
    basename="reviews",
)
router.register(
    r"titles/(?P<title_id>[\d.]+)/reviews",
    ReviewViewSet,
    basename="reviews",
)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", SingUpView.as_view(), name="singup"),
    path(
        "v1/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_access",
    ),
]
