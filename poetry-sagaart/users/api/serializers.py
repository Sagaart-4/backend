"""Модуль с сериализаторами для приложения users."""

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import BuyerProfile, CustomUser, SellerProfile
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


class BuyerProfileSerializer(serializers.ModelSerializer):
    """Получение списка или одного покупателя."""

    class Meta:
        """Класс с метаданными для сериализатора покупателя."""

        model = BuyerProfile
        exclude = ("user",)


class SellerProfileSerializer(serializers.ModelSerializer):
    """Получение списка или одного продавца."""

    class Meta:
        """Класс с метаданными для сериализатора продавца."""

        model = SellerProfile
        exclude = ("user",)


class CustomUserIsBuyerSerializer(UserSerializer):
    """Cериализатор для пользователя покупателя."""

    buyer_profile = BuyerProfileSerializer()

    class Meta:
        """Класс с метаданными для сериализатора пользователя+покупателя."""

        model = CustomUser
        fields = ("id", "email", "buyer_profile")
        read_only_fields = ("email",)

    def update(self, instance, validated_data):
        """Метод для обновления экземпляра модели профиля покупателя."""
        buyer_profile_attrs = validated_data.pop("buyer_profile", [])
        buyer_profile_instance = BuyerProfile.objects.get(user=instance.id)
        for attr, value in buyer_profile_attrs.items():
            setattr(buyer_profile_instance, attr, value)
            buyer_profile_instance.save()
        return instance


class CustomUserIsSellerSerializer(UserSerializer):
    """Cериализатор для пользователя продавца."""

    seller_profile = SellerProfileSerializer()

    class Meta:
        """Класс с метаданными для сериализатора пользователя+продавца."""

        model = CustomUser
        fields = ("id", "email", "seller_profile")
        read_only_fields = ("email",)

    def update(self, instance, validated_data):
        """Метод для обновления экземпляра модели профиля продавца."""
        seller_profile_attrs = validated_data.pop("seller_profile", [])
        seller_profile_instance = SellerProfile.objects.get(user=instance.id)
        for attr, value in seller_profile_attrs.items():
            setattr(seller_profile_instance, attr, value)
            seller_profile_instance.save()
        return instance
