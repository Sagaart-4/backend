from django.urls import path

from .views import (ArtistCreateView, FavoriteArtistCreateView,
                    FavoriteArtistDeleteView, FavoriteArtistListView)

urlpatterns = [
    path(
        'artist/',
        ArtistCreateView.as_view(),
        name='artist-create'
    ),
    path(
        'artists/favoriteArtist/',
        FavoriteArtistCreateView.as_view(),
        name='favorite-artist-create'
    ),
    path(
        'artists/favoriteArtist/<int:artistId>/<int:userId>/',
        FavoriteArtistDeleteView.as_view(),
        name='favorite-artist-delete'
    ),
    path(
        'artists/favoriteArtist/<int:userId>/',
        FavoriteArtistListView.as_view(),
        name='favorite-artist-list'
    ),
]
