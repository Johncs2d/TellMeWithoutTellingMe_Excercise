from django.shortcuts import render
from .category_view import CreateCategory, UpdateCategory, DeleteCategory, RetrieveCategories
from .item_view import CreateItem, UpdateItem, DeleteItem, RetrieveCategoryItems, RetrieveItemToGuess
from .score_view import SubmitScore, ListScores


def index(request):
    return render(request, 'templates/index.html', {})
