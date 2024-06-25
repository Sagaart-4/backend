"""Модуль с url-паттернами для приложения users."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.api.views import (
    BuyerProfileViewSet,
    CustomUserViewSet,
    SellerProfileViewSet,
)

v1_router = DefaultRouter()

v1_router.register("buyers", BuyerProfileViewSet, basename="buyers")
v1_router.register("sellers", SellerProfileViewSet, basename="sellers")
v1_router.register(r"users", CustomUserViewSet, basename="customuser")


urlpatterns = [
    path(
        "users/me/",
        CustomUserViewSet.as_view(
            {"get": "me", "patch": "me", "delete": "me"}
        ),
        name="me",
    ),
    path("", include(v1_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
