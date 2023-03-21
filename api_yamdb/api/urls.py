from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import SingUpView, CategoryViewSet, GenreViewSet, TitleViewSet

app_name = "api"

router = SimpleRouter()
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register("titles", TitleViewSet)

urlpatterns = [
    path("v1/auth/signup/", SingUpView.as_view(), name="singup"),
    path(
        "v1/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_access",
    ),
    path("v1/", include(router.urls)),
]
