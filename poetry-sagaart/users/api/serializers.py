"""Модуль с сериализаторами для приложения users."""

from api.serializers import CategorySerializer, StyleSerializer
from artshop.models import Category, Style, StyleBuyerProfile
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
    """Сериализатор для модели профиля покупателя."""

    lastName = serializers.CharField(source="surname")
    surname = serializers.CharField(source="patronymic_surname")
    phone = serializers.CharField(source="phone_number")
    preferStyle = serializers.CharField(source="favorite_style")
    preferCategory = serializers.CharField(source="favorite_category")
    preferStyles = StyleSerializer(many=True, source="favorite_styles")
    preferCategories = CategorySerializer(
        many=True, source="favorite_categories"
    )

    class Meta:
        """Класс с метаданными для сериализатора покупателя."""

        model = BuyerProfile
        fields = (
            "name",
            "lastName",
            "surname",
            "phone",
            "preferStyle",
            "preferCategory",
            "preferStyles",
            "preferCategories",
            "photo",
        )

        def update(self, instance, validated_data):
            """Метод для обновления экземпляра модели профиля покупателя."""
            styles = validated_data.pop("preferStyle")
            categories = validated_data.pop("preferCategory")
            buyer_profile_instance = SellerProfile.objects.get(
                user=instance.id
            )
            for style in styles:
                current_style, status = Style.objects.get_or_create(**style)
                StyleBuyerProfile.objects.create(
                    style=current_style, buyer_profile=buyer_profile_instance
                )
            for category in categories:
                current_category, status = Category.objects.get_or_create(
                    **category
                )
                StyleBuyerProfile.objects.create(
                    category=current_category,
                    buyer_profile=buyer_profile_instance,
                )
            return instance


class SellerProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для модели профиля продавца."""

    lastName = serializers.CharField(source="surname")
    surname = serializers.CharField(source="patronymic_surname")
    phone = serializers.CharField(source="phone_number")

    class Meta:
        """Класс с метаданными для сериализатора продавца."""

        model = SellerProfile
        fields = ("name", "lastName", "surname", "phone", "photo")


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
