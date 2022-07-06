import io

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tellme.models import Item, Category
from .category_view import CreateCategory, UpdateCategory, DeleteCategory, RetrieveCategories
from .item_view import CreateItem, UpdateItem, DeleteItem, RetrieveCategoryItems, RetrieveItemToGuess
from .score_view import SubmitScore, ListScores

from dependency_injector.wiring import inject, Provide

from src.containers import Container
from src.services import FileReaderService


@require_GET
def index(request):
    return render(request, 'templates/index.html', {})


@api_view(['POST'])
@inject
def upload(request, file_service: FileReaderService = Provide[Container.file_reader]):
    category = get_object_or_404(Category, pk=request.POST['category'])
    objects, data = file_service.to_model_objects(io.StringIO(request.FILES['file'].read().decode('utf-8')), Item, category=category)
    Item.objects.filter(category=category).delete()
    Item.objects.bulk_create(objects, batch_size=1000)
    return Response({"message": "Saved", "success": True, "data": data})
