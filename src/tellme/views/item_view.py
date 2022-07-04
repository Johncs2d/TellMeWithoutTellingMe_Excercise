from typing import Union

from django.db.models import QuerySet
from rest_framework import generics, serializers, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from tellme.serializers import ItemSerializer

from tellme.models import Item, Category


class CreateItem(generics.CreateAPIView):
    def __init__(self,
                 serializer_class: serializers.ModelSerializer = ItemSerializer,
                 permission_classes: Union[tuple, list] = (permissions.AllowAny,),
                 **kwargs
                 ):
        self.serializer_class = serializer_class
        self.permission_classes = permission_classes
        super().__init__(**kwargs)


class UpdateItem(generics.UpdateAPIView):
    def __init__(self,
                 serializer_class: serializers.ModelSerializer = ItemSerializer,
                 lookup_field: str = 'id',
                 queryset: QuerySet = Item.objects.all(),
                 permission_classes: Union[tuple, list] = (permissions.AllowAny,),
                 **kwargs
                 ):
        self.serializer_class = serializer_class
        self.lookup_field = lookup_field
        self.queryset = queryset
        self.permission_classes = permission_classes
        super().__init__(**kwargs)


class DeleteItem(generics.DestroyAPIView):
    def __init__(self,
                 serializer_class: serializers.ModelSerializer = ItemSerializer,
                 queryset: QuerySet = Item.objects.all(),
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


class RetrieveCategoryItems(generics.RetrieveAPIView):
    def __init__(self,
                 serializer_class: serializers.ModelSerializer = ItemSerializer,
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

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(self.get_queryset(), **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return Item.objects.filter(category=obj).order_by('?')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class RetrieveItemToGuess(generics.RetrieveAPIView):
    def __init__(self,
                 serializer_class: serializers.ModelSerializer = ItemSerializer,
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

    def get_queryset(self):
        return self.queryset

    def get_object(self):

        category = self.kwargs.get('id', 0)
        if category != 0:
            queryset = Category.objects.filter(pk=category).first()
        else:
            queryset = Category.objects.all().order_by('?')[:5]

        # May raise a permission denied
        self.check_object_permissions(self.request, queryset)

        if isinstance(queryset, QuerySet):
            return Item.objects.filter(category__in=queryset).order_by('?')

        return Item.objects.filter(category=queryset).order_by('?')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)
