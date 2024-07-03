from django.urls import path
from .views import DataView
# app_name = 'analytics'

urlpatterns = [
    path('user/analytics/', DataView.as_view, name='analytics'),
]
