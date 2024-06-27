"""Модуль с моделями для приложения artshop."""

from django.db import models
from users.models import BuyerProfile


class Style(models.Model):
    """Модель стиля произведения."""

    name = models.CharField(max_length=200)


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(max_length=200)


class StyleBuyerProfile(models.Model):
    """Ассоциативная таблица для стиля и профиля покупателя."""

    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    buyer_profile = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)

    def __str__(self):
        """Метод для вывода объекта модели на печать."""
        return f"{self.style} {self.buyer_profile}"


class CategoryBuyerProfile(models.Model):
    """Ассоциативная таблица для категории и профиля покупателя."""

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    buyer_profile = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)

    def __str__(self):
        """Метод для вывода объекта модели на печать."""
        return f"{self.category} {self.buyer_profile}"
