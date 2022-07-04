import functools
import random
from datetime import timedelta
from unittest.mock import patch

import factory
from django.urls import reverse
from rest_framework import status, permissions
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from faker import Faker

from tellme.models import Score

from tellme.views import ListScores
from . import CategoryFactory, create_category_items

fake = Faker()


class ScoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Score

    name = factory.Faker('name')
    time = timedelta(seconds=random.randint(20, 60))
    score = random.randint(1, 10)


class GamePlayTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_item_to_guess_ok(self):
        category = CategoryFactory(name='Jobs')
        items = create_category_items(50, category=category)
        path_name = 'tellme:RetrieveItemToGuess'
        url = reverse(path_name, kwargs={'id': category.id})
        req = self.client.get(url)

        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(len(req.json()), len(items))

        create_category_items(15, name=factory.Faker('name'), category=CategoryFactory(name='People Name'))

        url = reverse(path_name, kwargs={'id': 0})

        req = self.client.get(url)

        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(len(req.json()), 65)

        category_stub = CategoryFactory.stub(id=random.randint(100, 1000))
        url = reverse(path_name, kwargs={'id': category_stub.id})
        req = self.client.get(url)
        self.assertEqual(len(req.json()), 0)

    def test_submit_score_ok(self):
        category = CategoryFactory(name='Jobs')

        req = self.client.post('/api/score/', {
            'category': category.id,
            'name': 'JAB',
            'time': 10,
            'score': 10
        }, format='json')

        self.assertEqual(req.status_code, status.HTTP_201_CREATED)

    def test_retrieve_score_ok(self):
        ScoreFactory.create_batch(15)
        url = reverse('tellme:ListScores')
        req = self.client.get(url)
        self.assertEqual(len(req.json()), 15)
        self.assertEqual(req.status_code, status.HTTP_200_OK)

        with patch.object(ListScores, "get_queryset",
                          return_value=Score.objects.all().order_by('-date_created')[:1]) as mock_method:
            req = self.client.get(url)
            self.assertEqual(len(req.json()), 1)

            self.assertEqual(req.status_code, status.HTTP_200_OK)
            mock_method.assert_called()
