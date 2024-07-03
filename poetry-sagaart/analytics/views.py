from rest_framework import viewsets
from rest_framework.response import Response
from .Paintings_v2 import price_generator
from .models import Data
import numpy as np
from rest_framework.permissions import AllowAny


class DataView(viewsets.ViewSet):
    """Представление для расчета стоимости."""
    
    permission_classes = [AllowAny,]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос для цены."""
        data = Data(
            category=request.data.get('category', np.NaN),
            year=request.data.get('year', np.NaN),
            height=request.data.get('height', np.NaN),
            width=request.data.get('width', np.NaN),
            work_material=request.data.get('work_material', np.NaN),
            pad_material=request.data.get('pad_material', np.NaN),
            country=request.data.get('country', np.NaN),
            sex=request.data.get('sex', np.NaN),
            solo_shows=', '.join(request.data.get('solo_shows', np.NaN)),
            group_shows=', '.join(request.data.get('group_shows', np.NaN)),
            age=request.data.get('age', np.NaN),
        )

        price = price_generator(data.art_data())

        return Response(
            {
                "estimatedPrice": price,
            }
        )
