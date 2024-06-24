"""Модуль с сериализаторами для приложения users."""

from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from users.models import Buyer, CustomUser, Seller
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


class BuyerSerializer(serializers.ModelSerializer):
    """Получение списка или одного покупателя."""

    class Meta:
        """Класс с метаданными для сериализатора покупателя."""

        model = Buyer
        fields = "__all__"


class SellerSerializer(serializers.ModelSerializer):
    """Получение списка или одного продавца."""

    class Meta:
        """Класс с метаданными для сериализатора продавца."""

        model = Seller
        fields = "__all__"
