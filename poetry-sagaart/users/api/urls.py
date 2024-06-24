"""Модуль с url-паттернами для приложения users."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.api.views import BuyerViewSet, SellerViewSet

v1_router = DefaultRouter()

v1_router.register("buyers", BuyerViewSet, basename="buyers")
v1_router.register("sellers", SellerViewSet, basename="sellers")

urlpatterns = [
    path("", include(v1_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
