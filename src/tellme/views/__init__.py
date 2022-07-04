from django.shortcuts import render
from django.views.decorators.http import require_GET

from .category_view import CreateCategory, UpdateCategory, DeleteCategory, RetrieveCategories
from .item_view import CreateItem, UpdateItem, DeleteItem, RetrieveCategoryItems, RetrieveItemToGuess
from .score_view import SubmitScore, ListScores

@require_GET
def index(request):
    return render(request, 'templates/index.html', {})
