"""Модуль с сериализаторами для приложения users."""

from djoser.serializers import UserCreateSerializer
from users.models import CustomUser
from users.utils import create_user_with_account


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания новых пользователей."""

    class Meta:
        """Класс с метаданными для сериализатора создания пользователя."""

        model = CustomUser
        fields = ("email", "password", "role")

    def perform_create(self, validated_data):
        """Метод для создания пользователя с аккаунтом."""
        return create_user_with_account(validated_data)
