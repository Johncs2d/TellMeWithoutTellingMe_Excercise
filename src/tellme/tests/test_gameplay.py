import functools
import random
from datetime import timedelta

import factory
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from faker import Faker

from tellme.models import Score
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

        req = self.client.get('/api/item/guess/{}'.format(category.id))

        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(len(req.json()), len(items))

        create_category_items(15, name=factory.Faker('name'), category=CategoryFactory(name='People Name'))

        req = self.client.get('/api/item/guess/{}'.format(0))

        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(len(req.json()), 65)

        category_stub = CategoryFactory.stub(id=random.randint(100, 1000))
        req = self.client.get('/api/item/guess/{}'.format(category_stub.id))
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

        req = self.client.get('/api/scores')
        self.assertEqual(len(req.json()), 15)
