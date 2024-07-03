# Generated by Django 4.1 on 2024-07-03 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "artist_id",
                    models.AutoField(
                        help_text="Уникальный идентификатор художника",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "first_name",
                    models.CharField(help_text="Имя художника", max_length=100),
                ),
                (
                    "last_name",
                    models.CharField(help_text="Фамилия художника", max_length=100),
                ),
                (
                    "pseudonym",
                    models.CharField(
                        blank=True,
                        help_text="Псевдоним художника",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        help_text="Фотография художника",
                        null=True,
                        upload_to="artists/photos/",
                    ),
                ),
                (
                    "biography",
                    models.TextField(
                        blank=True, help_text="Биография художника", null=True
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Other", "Other"),
                        ],
                        help_text="Пол художника",
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "birth_year",
                    models.IntegerField(
                        blank=True, help_text="Год рождения художника", null=True
                    ),
                ),
                (
                    "birth_city",
                    models.CharField(
                        blank=True,
                        help_text="Город рождения художника",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "residence_city",
                    models.CharField(
                        blank=True,
                        help_text="Город проживания художника",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "education",
                    models.CharField(
                        blank=True,
                        help_text="Образование художника",
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "art_education",
                    models.CharField(
                        blank=True,
                        help_text="Художественное образование художника",
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "teaching_experience",
                    models.CharField(
                        blank=True,
                        help_text="Опыт преподавания художника",
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "personal_style",
                    models.CharField(
                        blank=True,
                        help_text="Персональный стиль художника",
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "individual_exhibitions",
                    models.TextField(
                        blank=True,
                        help_text="Индивидуальные показы художника",
                        null=True,
                    ),
                ),
                (
                    "group_exhibitions",
                    models.TextField(
                        blank=True, help_text="Групповые показы художника", null=True
                    ),
                ),
                (
                    "private_collections",
                    models.TextField(
                        blank=True,
                        help_text="Включение работ в частные коллекции",
                        null=True,
                    ),
                ),
                (
                    "institution_inclusion",
                    models.TextField(
                        blank=True,
                        help_text="Включение работ в коллекции учреждений",
                        null=True,
                    ),
                ),
                (
                    "industry_awards",
                    models.TextField(
                        blank=True,
                        help_text="Обладание высшими отраслевыми наградами",
                        null=True,
                    ),
                ),
                (
                    "vk_link",
                    models.URLField(
                        blank=True, help_text="Ссылка на VK художника", null=True
                    ),
                ),
                (
                    "telegram_link",
                    models.URLField(
                        blank=True, help_text="Ссылка на Telegram художника", null=True
                    ),
                ),
                (
                    "average_work_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Средняя стоимость работ художника",
                        max_digits=10,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Автор",
                "verbose_name_plural": "Авторы",
            },
        ),
        migrations.CreateModel(
            name="FavoriteArtist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="artist.artist",
                        verbose_name="Автор",
                    ),
                ),
            ],
            options={
                "verbose_name": "Любимый автор",
                "verbose_name_plural": "Любимые авторы",
            },
        ),
    ]
