from django.urls import path
from . import views

app_name = "tellme"
version = 1

urlpatterns = [
    path("category/", views.CreateCategory.as_view(), name="CreateCategory"),
    path("category/<int:id>/", views.UpdateCategory.as_view(), name="UpdateCategory"),
    path("category/remove/", views.DeleteCategory.as_view(), name="DeleteCategory"),
    path("categories", views.RetrieveCategories.as_view(), name="RetrieveCategories"),

    path("item/", views.CreateItem.as_view(), name="CreateItem"),
    path("item/<int:id>/", views.UpdateItem.as_view(), name="UpdateItem"),
    path("item/remove/", views.DeleteItem.as_view(), name="DeleteItem"),
    path("item/<int:id>", views.RetrieveCategoryItems.as_view(), name="RetrieveCategoryItems"),
]