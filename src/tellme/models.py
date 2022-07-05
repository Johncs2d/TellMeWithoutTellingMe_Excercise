from django.db import models
from django.db.models.manager import Manager
# Create your models here.
from tellme.managers import ScoreManager

from tellme.queryset import ScoreQuerySet


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, help_text="Category Name")
    description = models.TextField(null=True, blank=True)
    image_link = models.TextField(default='https://images.unsplash.com/photo-1618022325802-7e5e732d97a1?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=748&q=80', blank=True)
    objects = Manager()

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, help_text="Item Name")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='Item Category', blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    objects = Manager()

class Score(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, help_text="Player/Team Name")
    time = models.DurationField(null=True, blank=True, help_text="Game Duration")
    score = models.IntegerField(default=0, blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, blank=True, null=True, help_text="Category Selected")
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    objects = ScoreManager.from_queryset(ScoreQuerySet)()