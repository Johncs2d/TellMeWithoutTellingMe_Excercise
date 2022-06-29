from django.shortcuts import render
from rest_framework import generics, permissions, serializers, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Category, Item, Score
from .serializers import CategorySerializer, ItemSerializer, ScoreSerializer
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
    serializer_class = ItemSerializer

class UpdateItem(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ItemSerializer
    lookup_field = 'id'
    queryset = Item.objects.all()

class DeleteItem(generics.DestroyAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.request.data.get('id', None))

class RetrieveCategoryItems(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ItemSerializer
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

class RetrieveItemToGuess(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ItemSerializer
    queryset = Category.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        category = self.kwargs.get('id', 0)
        if category != 0:
            queryset = Category.objects.filter(pk=category).first()
        else:
            queryset = Category.objects.all().order_by('?').first()

        # May raise a permission denied
        self.check_object_permissions(self.request, queryset)
        return Item.objects.filter(category=queryset).order_by('?').first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class SubmitScore(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ScoreSerializer

class ListScores(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ScoreSerializer
    queryset = Score.objects.all()