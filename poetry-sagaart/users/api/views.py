"""Модуль с представлениями для приложения users."""

from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.api.serializers import (
    BuyerProfileSerializer,
    SellerProfileSerializer,
)
from users.models import BuyerProfile, CustomUser, SellerProfile


class CustomUserViewSet(UserViewSet):
    """Вьюсет для модели пользователей."""

    def get_queryset(self):
        """Метод для получения queryset-а пользователя."""
        user = self.request.user
        if user.role == "seller":
            return CustomUser.objects.select_related("seller_profile").all()
        return CustomUser.objects.select_related("buyer_profile").all()

    def get_serializer_class(self):
        """Метод для определения класса сериализатора."""
        if self.action == "create":
            if settings.USER_CREATE_PASSWORD_RETYPE:
                return settings.SERIALIZERS.user_create_password_retype
            return settings.SERIALIZERS.user_create
        elif self.action == "destroy" or (
            self.action == "me"
            and self.request
            and self.request.method == "DELETE"
        ):
            return settings.SERIALIZERS.user_delete
        elif self.action == "activation":
            return settings.SERIALIZERS.activation
        elif self.action == "resend_activation":
            return settings.SERIALIZERS.password_reset
        elif self.action == "reset_password":
            return settings.SERIALIZERS.password_reset
        elif self.action == "reset_password_confirm":
            if settings.PASSWORD_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.password_reset_confirm_retype
            return settings.SERIALIZERS.password_reset_confirm
        elif self.action == "set_password":
            if settings.SET_PASSWORD_RETYPE:
                return settings.SERIALIZERS.set_password_retype
            return settings.SERIALIZERS.set_password
        elif self.action == "set_username":
            if settings.SET_USERNAME_RETYPE:
                return settings.SERIALIZERS.set_username_retype
            return settings.SERIALIZERS.set_username
        elif self.action == "reset_username":
            return settings.SERIALIZERS.username_reset
        elif self.action == "reset_username_confirm":
            if settings.USERNAME_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.username_reset_confirm_retype
            return settings.SERIALIZERS.username_reset_confirm
        elif self.action == "me" and self.request.user.role == "buyer":
            return settings.SERIALIZERS.current_user_buyer
        elif self.action == "me" and self.request.user.role == "seller":
            return settings.SERIALIZERS.current_user_seller

        return self.serializer_class

    def destroy(self, request, *args, **kwargs):
        """Метод для удаления аккаунта текущего пользователя."""
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SellerProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели профиля продавца."""

    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    # pagination_class = CustomizedPaginator
    permission_classes = (AllowAny,)


class BuyerProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели профиля покупателя."""

    queryset = BuyerProfile.objects.all()
    serializer_class = BuyerProfileSerializer
    # pagination_class = CustomizedPaginator
    permission_classes = (AllowAny,)
