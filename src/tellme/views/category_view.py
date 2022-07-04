from typing import Union

from django.db.models import QuerySet
from rest_framework import serializers, generics, permissions
from rest_framework.generics import get_object_or_404

from tellme.models import Category
from tellme.serializers import CategorySerializer


class CreateCategory(generics.CreateAPIView):
    def __init__(self,
                 serializer_class: serializers.ModelSerializer = CategorySerializer,
                 permission_classes: Union[tuple, list] = (permissions.AllowAny,),
                 **kwargs
                 ):
        self.serializer_class = serializer_class
        self.permission_classes = permission_classes
        super().__init__(**kwargs)


class UpdateCategory(generics.UpdateAPIView):
    def __init__(self,
                 serializer_class: serializers.ModelSerializer = CategorySerializer,
                 lookup_field: str = 'id',
                 queryset: QuerySet = Category.objects.all(),
                 permission_classes: Union[tuple, list] = (permissions.AllowAny,),
                 **kwargs
                 ):
        self.serializer_class = serializer_class
        self.lookup_field = lookup_field
        self.queryset = queryset
        self.permission_classes = permission_classes
        super().__init__(**kwargs)


class DeleteCategory(generics.DestroyAPIView):
    def __init__(self,
                 serializer_class: serializers.ModelSerializer = CategorySerializer,
                 queryset: QuerySet = Category.objects.all(),
                 permission_classes: Union[tuple, list] = (permissions.AllowAny,),
                 **kwargs
                 ):
        self.serializer_class = serializer_class
        self.queryset = queryset
        self.permission_classes = permission_classes
        super().__init__(**kwargs)

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.request.data.get('id', None))


class RetrieveCategories(generics.ListAPIView):
    def __init__(self,
                 serializer_class: serializers.ModelSerializer = CategorySerializer,
                 queryset: QuerySet = Category.objects.all(),
                 permission_classes: Union[tuple, list] = (permissions.AllowAny,),
                 **kwargs
                 ):
        self.serializer_class = serializer_class
        self.queryset = queryset
        self.permission_classes = permission_classes
        super().__init__(**kwargs)
