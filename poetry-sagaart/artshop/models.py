"""Модуль с моделями для приложения artshop."""

from django.db import models


class Style(models.Model):
    """Модель стиля произведения."""

    name = models.CharField(max_length=200)


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(max_length=200)
