"""Модуль с кастомными моделями для приложения users."""

# from artshop.models import Category, Style
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

# from artshop.models import StyleBuyerProfile, CategoryBuyerProfile

USER_SURNAME_LENGTH = 150
USER_PATRONYMIC_LENGTH = 150
USER_NAME_LENGTH = 150
EMAIL_LENGTH = 254
PASSWORD_LENGTH = 150
ROLE_LENGTH = 15
STYLE_NAME_LENGTH = 50
CATEGORY_NAME_LENGTH = 50


class CustomUserManager(BaseUserManager):
    """Менеджер пользовательских моделей для кастомной модели пользователя."""

    def create_user(self, email, password, role, **extra_fields):
        """Метод создания пользователя."""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, password=None, role="moderator", **extra_fields
    ):
        """Метод создания суперпользователя."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, role, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя."""

    ROLE_CHOICES = (
        ("moderator", "Moderator"),
        ("buyer", "Buyer"),
        ("seller", "Seller"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    password = models.CharField(
        max_length=PASSWORD_LENGTH,
        verbose_name="password",
    )
    role = models.CharField(max_length=ROLE_LENGTH, choices=ROLE_CHOICES)
    email = models.EmailField(
        max_length=50,
        validators=[MinLengthValidator(6)],
        verbose_name="email",
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        """Класс с метаданными для модели пользователя."""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        unique_together = ("role", "email")

    def __str__(self):
        """Метод для вывода пользователя на печать."""
        return f"{self.role} {self.email}"


class BuyerProfile(models.Model):
    """Модель профиля покупателя."""

    user = models.OneToOneField(
        CustomUser,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="buyer_profile",
        primary_key=True,
    )
    name = models.CharField(
        max_length=USER_NAME_LENGTH,
        verbose_name="name",
    )
    surname = models.CharField(
        max_length=USER_SURNAME_LENGTH,
        verbose_name="surname",
    )
    patronymic_surname = models.CharField(
        max_length=USER_PATRONYMIC_LENGTH,
        verbose_name="patronymic_surname",
    )
    phone_number = models.CharField(
        max_length=20, help_text="Enter phone number"
    )
    favorite_styles = models.ManyToManyField(
        "artshop.Style",
        verbose_name="Любимые стили",
        through="artshop.StyleBuyerProfile",
    )
    favorite_style = models.CharField(
        max_length=STYLE_NAME_LENGTH,
        verbose_name="favorite_style",
    )
    favorite_categories = models.ManyToManyField(
        "artshop.Category",
        verbose_name="Любимые категории",
        through="artshop.CategoryBuyerProfile",
    )
    favorite_category = models.CharField(
        max_length=CATEGORY_NAME_LENGTH,
        verbose_name="favorite_category",
    )
    favorite_artists = models.ManyToManyField(
        "artist.Artist",
        verbose_name="Любимые художники",
        through="artist.FavoriteArtist",
    )
    photo = models.ImageField(
        upload_to="users_photos/",
        blank=True,
        null=True,
        verbose_name="аватар",
    )
    objects = models.Manager()

    def __str__(self):
        """Метод для вывода покупателя на печать."""
        return f"{self.name} {self.surname}"


class SellerProfile(models.Model):
    """Модель профиля продавца."""

    user = models.OneToOneField(
        CustomUser,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="seller_profile",
        primary_key=True,
    )
    name = models.CharField(
        max_length=USER_NAME_LENGTH,
        verbose_name="name",
    )
    surname = models.CharField(
        max_length=USER_SURNAME_LENGTH,
        verbose_name="surname",
    )
    patronymic_surname = models.CharField(
        max_length=USER_PATRONYMIC_LENGTH,
        verbose_name="patronymic_surname",
    )
    phone_number = models.CharField(
        max_length=20, help_text="Enter phone number"
    )
    photo = models.ImageField(
        upload_to="users_photos/",
        blank=True,
        null=True,
        verbose_name="аватар",
    )
    objects = models.Manager()

    def __str__(self):
        """Метод для вывода продавца на печать."""
        return f"{self.name} {self.surname}"


class Subscription(models.Model):
    """Модель подписки на расширенный функционал сайта."""

    STATUS_CHOICES = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("canceled", "Canceled"),
    )

    id = models.AutoField(primary_key=True, unique=True)
    user_id = models.ForeignKey(
        BuyerProfile,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="подписчик",
    )
    auto_renewal = models.BooleanField(default=False)
    duration = models.IntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
