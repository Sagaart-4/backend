from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Artist, BuyerProfile as User, FavoriteArtist
from .serializers import ArtistSerializer, FavoriteArtistSerializer


class ArtistCreateView(APIView):
    """Представление для создания нового художника."""

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос для создания нового художника."""
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            artist = serializer.save()
            return Response({
                "ArtistID": artist.artist_id,
                "message": "Художник успешно создан"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteArtistCreateView(APIView):
    """Представление для добавления художника в избранное."""

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос для добавления художника в избранное."""
        artist_id = request.data.get('artistID')
        user_id = request.data.get('userID')
        artist = get_object_or_404(Artist, artist_id=artist_id)
        user = get_object_or_404(User, pk=user_id)

        if FavoriteArtist.objects.filter(artist=artist, user=user).exists():
            return Response({
                "error": "Артист уже добавлен в избранное"
            }, status=status.HTTP_409_CONFLICT)

        favorite_artist = FavoriteArtist.objects.create(
            artist=artist, user=user
        )
        return Response({
            "artistID": favorite_artist.artist.artist_id,
            "userID": favorite_artist.user.id,
            "message": "Артист добавлен в избранное"
        }, status=status.HTTP_201_CREATED)


class FavoriteArtistDeleteView(APIView):
    """Представление для удаления художника из избранного."""

    def delete(self, request, artistId, userId, *args, **kwargs):
        """Обрабатывает DELETE-запрос для удаления художника из избранного."""
        artist = get_object_or_404(Artist, artist_id=artistId)
        user = get_object_or_404(User, pk=userId)
        favorite_artist = get_object_or_404(
            FavoriteArtist,
            artist=artist,
            user=user
        )
        favorite_artist.delete()
        return Response({
            "message": "Артист успешно удален из избранного"
        }, status=status.HTTP_200_OK)


class FavoriteArtistListView(APIView):
    """Представление для просмотра списка избранных художников."""

    def get(self, request, userId, *args, **kwargs):
        """Обрабатывает GET-запрос для получения списка избранных художников"""
        user = get_object_or_404(User, pk=userId)
        favorite_artists = FavoriteArtist.objects.filter(user=user)

        if not favorite_artists:
            return Response({
                "error": "Избранные артисты отсутствуют"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = FavoriteArtistSerializer(favorite_artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
