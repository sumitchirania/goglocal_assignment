from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoginView, MyProfileView, CurrentUserViewSet

router = DefaultRouter()
router.register("user/all-users", CurrentUserViewSet, basename="user")

urlpatterns = [
    path("user/login/", LoginView.as_view(), name="login"),
    path("user/profile/", MyProfileView.as_view(), name="login"),
    ]

urlpatterns += router.urls


