from rest_framework import serializers
from .models import Artist, FavoriteArtist


class ArtistSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Artist, который преобразует данные из модели
    в JSON-формат и наоборот, с изменением имен полей.
    """

    lastnameArtist = serializers.CharField(
        source="last_name"
    )
    nameArtist = serializers.CharField(
        source="first_name"
    )
    pseudonym = serializers.CharField(
        source="pseudonym"
    )
    fotoArtist = serializers.ImageField(
        source="photo"
    )
    biography = serializers.CharField(
        source="biography"
    )
    gender = serializers.CharField(
        source="gender"
    )
    yearOfBirth = serializers.IntegerField(
        source="birth_year"
    )
    cityOfBirth = serializers.CharField(
        source="birth_city"
    )
    cityOfResidence = serializers.CharField(
        source="residence_city"
    )
    education = serializers.CharField(
        source="education"
    )
    artEducation = serializers.CharField(
        source="art_education"
    )
    teachingExperience = serializers.CharField(
        source="teaching_experience"
    )
    personalStyle = serializers.CharField(
        source="personal_style"
    )
    soloShows = serializers.CharField(
        source="individual_exhibitions"
    )
    groupShows = serializers.CharField(
        source="group_exhibitions"
    )
    collectedByPrivateCollectors = serializers.BooleanField(
        source="private_collections"
    )
    collectedByMajorInstitution = serializers.CharField(
        source="institution_inclusion"
    )
    winnerTopIndustry = serializers.CharField(
        source="industry_awards"
    )
    socmediaLinkTg = serializers.URLField(
        source="telegram_link"
    )
    socmediaLinkVk = serializers.URLField(
        source="vk_link"
    )

    class Meta:
        model = Artist
        fields = [
            'lastnameArtist', 'nameArtist', 'pseudonym', 'fotoArtist',
            'biography', 'gender', 'yearOfBirth', 'cityOfBirth',
            'cityOfResidence', 'education', 'artEducation',
            'teachingExperience', 'personalStyle', 'soloShows', 'groupShows',
            'collectedByPrivateCollectors', 'collectedByMajorInstitution',
            'winnerTopIndustry', 'socmediaLinkTg', 'socmediaLinkVk'
        ]


class FavoriteArtistSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели FavoriteArtist, который преобразует данные из
    модели в JSON-формат и наоборот, с изменением имен полей.
    """

    artistID = serializers.IntegerField(source='artist.id')
    userID = serializers.IntegerField(source='user.id')

    class Meta:
        model = FavoriteArtist
        fields = ['artistID', 'userID']
