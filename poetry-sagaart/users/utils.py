"""Модуль с функциями для приложения users."""

from django.db import transaction
from users.models import BuyerProfile, SellerProfile

from .models import CustomUser


@transaction.atomic
def create_user_with_account(validated_data: dict) -> CustomUser:
    """Создание пользователя с профилем в соответствии с выбранной ролью."""
    user = CustomUser.objects.create_user(**validated_data)
    role = validated_data.get("role")
    if role == "buyer":
        BuyerProfile.objects.create(user=user)
    if role == "seller":
        SellerProfile.objects.create(user=user)
    user.is_active = True
    user.save()
    return user
