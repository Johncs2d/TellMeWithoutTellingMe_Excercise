import functools
from unittest.mock import MagicMock, patch

from django.urls import reverse
from rest_framework import status, permissions
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from tellme.models import Category
import factory
from faker import Faker

from tellme.views import CreateCategory

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'Category-{}'.format(n))
    description = factory.Faker('text')


class CategoryTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_category_creation_ok(self):
        url = reverse('tellme:CreateCategory')
        req = self.client.post(url, {
            'name': 'Animals',
            'description': fake.text()
        }, format='json')
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(pk=req.json()['id']).exists(), True)

    def test_category_creation_not_ok(self):
        url = reverse('tellme:CreateCategory')
        post = functools.partial(self.client.post, path=url, data={'description': fake.text()},
                                 format='json')
        get = functools.partial(self.client.get, path=url, data={'description': fake.text()},
                                format='json')

        self.assertEqual(post().status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(post(path='/api/categories/').status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get().status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        view = CreateCategory.as_view(permission_classes=(permissions.IsAuthenticated,))
        request = self.factory.post(url, data={'description': fake.text(), 'name': 'Test'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_retrieve_ok_200(self):
        categories = CategoryFactory.create_batch(10)

        req = self.client.get('/api/categories')
        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(len(categories), len(req.json()))

    def test_category_update_category_name_ok(self):
        category = CategoryFactory()
        url = reverse('tellme:UpdateCategory', kwargs={'id': category.id})
        req = self.client.patch(url, {
            'name': 'People',
        }, format='json')
        self.assertEqual(req.json()['name'], 'People')
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def test_category_update_category_name_not_ok(self):
        url = reverse('tellme:UpdateCategory', kwargs={'id': 0})
        patch = functools.partial(self.client.patch, path=url, data={'name': 'People', },
                                  format='json')
        get = functools.partial(self.client.get, path=url, data={'description': fake.text()},
                                format='json')

        self.assertEqual(patch().status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get().status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_category_destroy_not_ok(self):
        url = reverse('tellme:DeleteCategory')
        delete = functools.partial(self.client.delete, path=url, data={'id': 0}, format='json')
        get = functools.partial(self.client.get, path=url, data={'id': 0}, format='json')

        self.assertEqual(delete().status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(delete(path='/api/category/remove').status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.assertEqual(get().status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_category_destroy_ok(self):
        category = CategoryFactory()
        url = reverse('tellme:DeleteCategory')
        req = self.client.delete(url, {'id': category.id}, format='json')

        self.assertEqual(req.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.filter(pk=category.id).exists(), False)
