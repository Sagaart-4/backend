"""Модуль с представлениями для приложения users."""

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from users.api.serializers import BuyerSerializer, SellerSerializer
from users.models import Buyer, Seller


class SellerViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для кастомной модели пользователя."""

    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    # pagination_class = CustomizedPaginator
    permission_classes = (AllowAny,)


class BuyerViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для кастомной модели пользователя."""

    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    # pagination_class = CustomizedPaginator
    permission_classes = (AllowAny,)
