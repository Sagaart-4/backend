"""Модуль с сериализаторами для приложения users."""

from api.serializers import CategorySerializer, StyleSerializer
from artshop.models import Category, Style, StyleBuyerProfile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import BuyerProfile, CustomUser, SellerProfile, Subscription
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

    def to_representation(self, instance):
        """Метод для настройки отображения ответа."""
        data = super(CustomUserCreateSerializer, self).to_representation(
            instance
        )
        user_tokens = RefreshToken.for_user(instance)
        tokens = {
            "refresh": str(user_tokens),
            "access": str(user_tokens.access_token),
        }
        data = data | tokens
        return data


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания подписки."""

    userId = serializers.IntegerField(source="user_id")
    autoSubs = serializers.BooleanField(source="auto_renewal")
    subsPeriod = serializers.IntegerField(source="duration")
    subsDateOn = serializers.DateTimeField(source="start_date")

    class Meta:
        """Класс с метаданными для сериализатора подписки."""

        model = Subscription
        fields = ("userId", "autoSubs", "subsPeriod", "subsDateOn")


class SubscriptionGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения подписки."""

    subscriptionId = serializers.IntegerField(source="id")
    userId = serializers.IntegerField(source="user_id")
    autoSubs = serializers.BooleanField(source="auto_renewal")
    subsPeriod = serializers.IntegerField(source="duration")
    subsDateOn = serializers.DateTimeField(source="start_date")

    class Meta:
        """Класс с метаданными для сериализатора подписки."""

        model = Subscription
        fields = (
            "subscriptionId",
            "userId",
            "autoSubs",
            "subsPeriod",
            "subsDateOn",
        )


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
    subscription = SubscriptionGetSerializer(source="subscriptions")

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
            "subscription",
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
        fields = ("id", "email", "role", "buyer_profile")
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
        fields = ("id", "email", "role", "seller_profile")
        read_only_fields = ("email",)

    def update(self, instance, validated_data):
        """Метод для обновления экземпляра модели профиля продавца."""
        seller_profile_attrs = validated_data.pop("seller_profile", [])
        seller_profile_instance = SellerProfile.objects.get(user=instance.id)
        for attr, value in seller_profile_attrs.items():
            setattr(seller_profile_instance, attr, value)
            seller_profile_instance.save()
        return instance
