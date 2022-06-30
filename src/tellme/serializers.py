from rest_framework import serializers

from .models import Category, Item, Score


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'image_link',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        instance = Category.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance

class ItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'category'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'category': {'write_only': True, 'required': True},
        }

    def create(self, validated_data):
        instance = Item.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance

class ScoreSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField()
    class Meta:
        model = Score
        fields = [
            'id',
            'time',
            'name',
            'score',
            'category',
            'category_name',
            'date_created',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'category': {'write_only': True, 'required': False},
            'category_name': {'read_only': True},
        }

    def create(self, validated_data):
        instance = Score.objects.create(**validated_data)
        return instance
