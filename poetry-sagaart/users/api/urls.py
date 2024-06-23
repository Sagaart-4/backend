"""Модуль с url-паттернами для приложения users."""

from django.urls import include, path

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
