import functools
from unittest.mock import patch, Mock

import factory
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from tellme.models import Item, Category

from tellme.views import RetrieveCategoryItems
from . import CategoryFactory
from faker import Faker

fake = Faker()


class CategoryItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Faker('job')
    category = factory.SubFactory(CategoryFactory)


def create_category_items(count, name=factory.Faker('job'), **kwargs):
    return CategoryItemFactory.create_batch(count, name=name, **kwargs)


class CategoryItemTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_category_item_ok(self):
        category = CategoryFactory()

        req = self.client.post('/api/item/', {
            'name': 'Manila',
            'category': category.id
        }, format='json')

        self.assertEqual(req.status_code, status.HTTP_201_CREATED)
        self.assertEqual(req.json()['category'], category.id)
        self.assertEqual(req.json()['name'], 'Manila')
        self.assertEqual(Item.objects.filter(pk=req.json()['id']).exists(), True)

    def test_create_category_item_not_ok(self):
        category = CategoryFactory()

        post = functools.partial(self.client.post, path='/api/item/', data={'category': category.id}, format='json')
        get = functools.partial(self.client.get, path='/api/item/', data={'description': fake.text()}, format='json')

        self.assertEqual(post().status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(post(data={'category': 0, 'name': 'Manila'}).status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(post(path='/api/items/').status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get().status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_category_item_ok(self):
        item = CategoryItemFactory()

        req = self.client.patch('/api/item/{}/'.format(item.id), {
            'name': 'Manila Zoo',
        }, format='json')
        self.assertEqual(req.json()['name'], 'Manila Zoo')
        self.assertEqual(Item.objects.get(pk=item.id).name, 'Manila Zoo')
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def test_update_category_item_not_ok(self):
        item = CategoryItemFactory()
        item_stub = CategoryItemFactory.stub(id=0)

        patch = functools.partial(self.client.patch, path='/api/item/{}/'.format(item.id), data={'name': 'Manila Zoo'},
                                  format='json')
        get = functools.partial(self.client.get, path='/api/item/{}/'.format(item.id), data={'name': 'Manila Zoo'},
                                format='json')

        self.assertEqual(patch(path='/api/items/').status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(patch(path='/api/item/{}/'.format(item_stub.id)).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get().status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_category_item_ok(self):
        category = CategoryFactory()
        items = create_category_items(10, category=category)
        self.assertEqual(Item.objects.all().count(), 10)

        req = self.client.delete('/api/item/remove/', {'id': items[0].id, }, format='json')
        self.assertEqual(req.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.all().count(), 9)

    def test_delete_category_item_not_ok(self):
        delete = functools.partial(self.client.delete, path='/api/item/remove/', data={'id': 0}, format='json')
        get = functools.partial(self.client.get, path='/api/item/remove/', data={'id': 0}, format='json')

        self.assertEqual(delete().status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(delete(path='/api/item/remove').status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.assertEqual(get().status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_category_item_retrieve_ok(self):
        category = CategoryFactory()
        items = create_category_items(10, category=category)

        req = self.client.get('/api/item/{}'.format(category.id))
        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(len(items), len(req.json()))

        with patch.object(RetrieveCategoryItems, "get_object") as mock_method:
            factory = APIRequestFactory()
            view = RetrieveCategoryItems.as_view(queryset=Category.objects.filter(pk=category.id))
            request = factory.get('/api/item/{}/'.format(category.id), id=category.id)
            response = view(request, id=category.id)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            mock_method.assert_called()

    def test_category_item_retrieve_not_ok(self):
        category = CategoryFactory()
        create_category_items(10, category=category)

        item_stub = CategoryItemFactory.stub(id=0)

        req = self.client.get('/api/item/{}'.format(item_stub.id))

        self.assertEqual(req.status_code, status.HTTP_404_NOT_FOUND)
