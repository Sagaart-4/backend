"""Модуль с кастомными моделями для приложения users."""

from artshop.models import Category, Style
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

USER_SURNAME_LENGTH = 150
USER_PATRONYMIC_LENGTH = 150
USER_NAME_LENGTH = 150
EMAIL_LENGTH = 254
PASSWORD_LENGTH = 150
ROLE_LENGTH = 15


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

    def create_superuser(self, email, password=None, **extra_fields):
        """Метод создания суперпользователя."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
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
        unique=False,
        validators=[MinLengthValidator(6)],
        verbose_name="email",
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["email", "password", "role"]

    class Meta:
        """Класс с метаданными для модели пользователя."""

        unique_together = (
            "role",
            "email",
        )
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """Метод для вывода пользователя на печать."""
        return f"{self.role} {self.email}"


class Buyer(models.Model):
    """Модель покупателя."""

    user = models.OneToOneField(
        CustomUser,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="buyer_account",
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
        Style,
        verbose_name="Любимые стили",
    )
    favorite_categories = models.ManyToManyField(
        Category,
        verbose_name="Любимые категории",
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


class Seller(models.Model):
    """Модель продавца."""

    user = models.OneToOneField(
        CustomUser,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="seller_account",
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
