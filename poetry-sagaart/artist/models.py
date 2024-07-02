from django.db import models

from users.models import CustomUser as User


class Artist(models.Model):
    """Модель, представляющая художника с различными атрибутами."""

    artist_id = models.AutoField(
        primary_key=True,
        help_text="Уникальный идентификатор художника"
    )
    first_name = models.CharField(
        max_length=100,
        help_text="Имя художника"
    )
    last_name = models.CharField(
        max_length=100,
        help_text="Фамилия художника"
    )
    pseudonym = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Псевдоним художника"
    )
    photo = models.ImageField(
        upload_to='artists/photos/',
        blank=True,
        null=True,
        help_text="Фотография художника"
    )
    biography = models.TextField(
        blank=True,
        null=True,
        help_text="Биография художника"
    )
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=True, null=True,
        help_text="Пол художника"
    )
    birth_year = models.IntegerField(
        blank=True,
        null=True,
        help_text="Год рождения художника"
    )
    birth_city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Город рождения художника"
    )
    residence_city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Город проживания художника"
    )
    education = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Образование художника"
    )
    art_education = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Художественное образование художника"
    )
    teaching_experience = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Опыт преподавания художника"
    )
    personal_style = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Персональный стиль художника"
    )
    individual_exhibitions = models.TextField(
        blank=True,
        null=True,
        help_text="Индивидуальные показы художника"
    )
    group_exhibitions = models.TextField(
        blank=True,
        null=True,
        help_text="Групповые показы художника"
    )
    private_collections = models.TextField(
        blank=True,
        null=True,
        help_text="Включение работ в частные коллекции"
    )
    institution_inclusion = models.TextField(
        blank=True,
        null=True,
        help_text="Включение работ в коллекции учреждений"
    )
    industry_awards = models.TextField(
        blank=True,
        null=True,
        help_text="Обладание высшими отраслевыми наградами"
    )
    vk_link = models.URLField(
        blank=True,
        null=True,
        help_text="Ссылка на VK художника"
    )
    telegram_link = models.URLField(
        blank=True,
        null=True,
        help_text="Ссылка на Telegram художника"
    )
    average_work_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Средняя стоимость работ художника"
    )

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - ({self.pseudonym})"


class FavoriteArtist(models.Model):
    """Модель избранных художников."""

    artist = models.ForeignKey(
        Artist,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='favorite_artists'
    )
    user = models.ForeignKey(
        User,
        verbose_name='Ценитель автора',
        on_delete=models.CASCADE,
        related_name='favorite_artists'
    )

    class Meta:
        verbose_name = 'Любимый автор'
        verbose_name_plural = 'Любимые авторы'
        constraints = [
            models.UniqueConstraint(
                fields=('artist', 'user'), name='unique_favorite_artist'
            )
        ]

    def __str__(self):
        return f'{self.artist} в любимых авторах у {self.user}'
