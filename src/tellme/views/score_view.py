from typing import Union

from django.db.models import QuerySet
from rest_framework import generics, serializers, permissions

from tellme.serializers import ScoreSerializer

from tellme.models import Score


class SubmitScore(generics.CreateAPIView):
    def __init__(self,
                 serializer_class: serializers.ModelSerializer = ScoreSerializer,
                 permission_classes: Union[tuple, list] = (permissions.AllowAny,),
                 **kwargs
                 ):
        self.serializer_class = serializer_class
        self.permission_classes = permission_classes
        super().__init__(**kwargs)


class ListScores(generics.ListAPIView):
    def __init__(self,
                 serializer_class: serializers.ModelSerializer = ScoreSerializer,
                 queryset: QuerySet = Score.objects.fetch_latest(15),
                 permission_classes: Union[tuple, list] = (permissions.AllowAny,),
                 **kwargs
                 ):
        self.serializer_class = serializer_class

        self.queryset = queryset
        self.permission_classes = permission_classes
        super().__init__(**kwargs)
