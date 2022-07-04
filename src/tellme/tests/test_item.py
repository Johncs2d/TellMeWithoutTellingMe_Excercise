import functools
from unittest.mock import patch, Mock, MagicMock

import factory
from django.urls import reverse
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
        url = reverse('tellme:CreateItem')
        req = self.client.post(url, {
            'name': 'Manila',
            'category': category.id
        }, format='json')

        self.assertEqual(req.status_code, status.HTTP_201_CREATED)
        self.assertEqual(req.json()['category'], category.id)
        self.assertEqual(req.json()['name'], 'Manila')
        self.assertEqual(Item.objects.filter(pk=req.json()['id']).exists(), True)

    def test_create_category_item_not_ok(self):
        category = CategoryFactory()
        url = reverse('tellme:CreateItem')
        post = functools.partial(self.client.post, path=url, data={'category': category.id}, format='json')
        get = functools.partial(self.client.get, path=url, data={'description': fake.text()}, format='json')

        self.assertEqual(post().status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(post(data={'category': 0, 'name': 'Manila'}).status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(post(path='/api/items/').status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get().status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_category_item_ok(self):
        item = CategoryItemFactory()
        url = reverse('tellme:UpdateItem', kwargs={'id': item.id})
        name = 'Manila Zoo'
        req = self.client.patch(url, {
            'name': name,
        }, format='json')
        self.assertEqual(req.json()['name'], name)
        self.assertEqual(Item.objects.get(pk=item.id).name, name)
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def test_update_category_item_not_ok(self):
        name = 'Manila Zoo'
        item = CategoryItemFactory()
        item_stub = CategoryItemFactory.stub(id=0)
        url = reverse('tellme:UpdateItem', kwargs={'id': item.id})
        patch = functools.partial(self.client.patch, path=url, data={'name': name},
                                  format='json')
        get = functools.partial(self.client.get, path=url, data={'name': name},
                                format='json')

        self.assertEqual(patch(path='/api/items/').status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(patch(path='/api/item/{}/'.format(item_stub.id)).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get().status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_category_item_ok(self):
        category = CategoryFactory()
        items = create_category_items(10, category=category)
        self.assertEqual(Item.objects.all().count(), 10)
        url = reverse('tellme:DeleteItem')
        req = self.client.delete(url, {'id': items[0].id, }, format='json')
        self.assertEqual(req.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.all().count(), 9)

    def test_delete_category_item_not_ok(self):
        url = reverse('tellme:DeleteItem')
        delete = functools.partial(self.client.delete, path=url, data={'id': 0}, format='json')
        get = functools.partial(self.client.get, path=url, data={'id': 0}, format='json')

        self.assertEqual(delete().status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(delete(path='/api/item/remove').status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.assertEqual(get().status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_category_item_retrieve_ok(self):
        category = CategoryFactory()
        items = create_category_items(10, category=category)
        url = reverse('tellme:RetrieveCategoryItems', kwargs={'id': category.id})
        req = self.client.get(url)
        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(len(items), len(req.json()))

        with patch.object(RetrieveCategoryItems, "get_queryset", return_value=Category.objects.filter(pk=category.id)) as mock_method:
            factory = APIRequestFactory()
            view = RetrieveCategoryItems.as_view()
            request = factory.get(url, id=category.id)
            response = view(request, id=category.id)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            mock_method.assert_called()

    def test_category_item_retrieve_not_ok(self):
        category = CategoryFactory()
        create_category_items(10, category=category)

        item_stub = CategoryItemFactory.stub(id=0)
        url = reverse('tellme:RetrieveCategoryItems', kwargs={'id': item_stub.id})
        req = self.client.get(url)

        self.assertEqual(req.status_code, status.HTTP_404_NOT_FOUND)
