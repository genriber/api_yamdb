from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    SingUpView,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)

app_name = "api"

router = SimpleRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")
router.register("titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/auth/signup/", SingUpView.as_view(), name="singup"),
    path(
        "v1/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_access",
    ),
    path("v1/", include(router.urls)),
]
