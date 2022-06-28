from django.shortcuts import render
from rest_framework import generics, permissions, serializers, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Category, Item
from .serializers import CategorySerializer, ItemSerielizer
import random

# Create your views here.
def index(request):
    return render(request, 'templates/index.html', {})

class CreateCategory(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = CategorySerializer

class UpdateCategory(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = CategorySerializer
    lookup_field = 'id'
    queryset = Category.objects.all()

class DeleteCategory(generics.DestroyAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.request.data.get('id', None))

class RetrieveCategories(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CreateItem(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ItemSerielizer

class UpdateItem(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ItemSerielizer
    lookup_field = 'id'
    queryset = Item.objects.all()

class DeleteItem(generics.DestroyAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ItemSerielizer
    queryset = Item.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.request.data.get('id', None))

class RetrieveCategoryItems(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ItemSerielizer
    queryset = Category.objects.all()
    lookup_field = 'id'

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