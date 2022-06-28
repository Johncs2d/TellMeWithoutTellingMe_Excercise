from django.db import models
from django.db.models.manager import Manager
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, help_text="Category Name")
    description = models.TextField(null=True, blank=True)
    objects = Manager()

class Item(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, help_text="Item Name")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='Item Category', blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    objects = Manager()

class Score(models.Model):
    player = models.CharField(max_length=50, null=False, blank=False, help_text="Player Name")
    time = models.DurationField(null=True, blank=True, help_text="Game Duration")
    category = models.ForeignKey(to=Category, on_delete=models.RESTRICT, blank=False, null=False, help_text="Category Selected")
    answer = models.CharField(max_length=50, null=True, blank=True, help_text="Player Answer")
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    objects = Manager()