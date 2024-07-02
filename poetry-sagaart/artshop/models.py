"""Модуль с моделями для приложения artshop."""

from artist.models import Artist
from django.db import models
from django.db.models import UniqueConstraint
from users.models import BuyerProfile, SellerProfile

from artshop.validators import year_validator

SHORT_LENGTH = 64
STANDART_LENGTH = 128
DOUBLE_LENGTH = 256


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


class Product(models.Model):
    """Модель товара(художественного произведения)."""

    ORIENTATION_CHOICES = (
        ('horizontal', 'горизонтальная'),
        ('vertical', 'вертикальная'),
    )

    id = models.BigAutoField(primary_key=True, db_column="ProductID")
    seller = models.ForeignKey(
        SellerProfile, on_delete=models.CASCADE, db_column="SellerID"
    )
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, db_column="ArtistID"
    )
    created = models.DateTimeField(
        auto_now_add=True, db_column="dateTimeOfCreation"
    )
    type = models.CharField(
        max_length=STANDART_LENGTH, db_column="typeProduct"
    )
    title = models.CharField(max_length=STANDART_LENGTH, db_column="titleArt")
    description = models.TextField(
        max_length=DOUBLE_LENGTH, db_column="description"
    )
    moderation_status = models.BooleanField(
        default=False, db_column="moderationStatus"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, db_column="categoryArt"
    )
    style = models.ForeignKey(
        Style, on_delete=models.SET_NULL, db_column="styleArt"
    )
    colour = models.CharField(max_length=STANDART_LENGTH, db_column="colorArt")
    year_of_creation = models.PositiveSmallIntegerField(
        validators=[year_validator],
        db_column="yearofCreation",
        help_text="Используйте слудующий формат: <YYYY>",
    )
    orientation = models.CharField(
        choices=ORIENTATION_CHOICES,
        max_length=SHORT_LENGTH,
        db_column="orientalProduct",
    )
    width = models.PositiveIntegerField(db_column="widthMm")
    height = models.PositiveIntegerField(db_column="heightMm")
    material = models.CharField(
        max_length=STANDART_LENGTH, db_column="atrMaterial"
    )
    frame = models.CharField(
        max_length=STANDART_LENGTH, db_column="frameMaterial"
    )
    signature = models.CharField(
        max_length=STANDART_LENGTH, db_column="signatureArt"
    )
    price_desired = models.PositiveIntegerField(db_column="desiredPrice")
    price_estimated = models.PositiveIntegerField(db_column="estimatedPrice")
    price_forecast = models.PositiveIntegerField(db_column="forecastPrice")

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        """Метод для вывода объекта модели на печать."""
        return f"{self.title}"


class Favorites(models.Model):
    """Модель избранного у покупателя."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="favorite_arts",
        db_column="ProductID",
    )
    user = models.ForeignKey(
        BuyerProfile,
        on_delete=models.CASCADE,
        related_name="favorite_arts",
        db_column="UserID",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                name="unique_favorite",
                fields=["product", "user"],
            )
        ]
        ordering = ("product",)

    def __str__(self):
        return f" Картина {self.product} добавлена пользователем {self.user}."
