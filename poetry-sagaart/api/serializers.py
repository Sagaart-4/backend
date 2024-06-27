"""Модуль с сериализаторами для моделей стилей и категорий."""

from artshop.models import Category, Style
from rest_framework import serializers


class StyleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели стилей."""

    class Meta:
        """Класс с метаданными для сериализатора стилей."""

        model = Style
        fields = ("name",)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категорий."""

    class Meta:
        """Класс с метаданными для сериализатора категорий."""

        model = Category
        fields = ("name",)
