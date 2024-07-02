"""Модуль содержащий класс для работы с разрешениями."""

from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """Класс для проверки наличия автора или администратора."""

    def has_permission(self, request, view):
        """Метод для проверки наличия разрешения."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Метод для проверки наличия разрешения на действия с объектом."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
