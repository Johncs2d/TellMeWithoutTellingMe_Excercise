import functools
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status, permissions, serializers
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate

from tellme.models import Category
import factory
from faker import Faker

from tellme.views import CreateCategory, DeleteCategory, UpdateCategory

from tellme.serializers import CategorySerializer

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

        error = serializers.ValidationError({'message': 'Test Mock Error Raised'})
        error.status_code = status.HTTP_406_NOT_ACCEPTABLE

        with patch.object(CategorySerializer, "create", side_effect=error):
            req = self.client.post(url, data={'description': fake.text(), 'name': fake.name()}, format='json')
            self.assertEqual(req.status_code, status.HTTP_406_NOT_ACCEPTABLE)
            self.assertEqual(req.json(), {'message': 'Test Mock Error Raised'})

        view = CreateCategory.as_view(permission_classes=(permissions.IsAuthenticated,))
        request = self.factory.post(url, data={'description': fake.text(), 'name': fake.name()})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_retrieve_ok_200(self):
        categories = CategoryFactory.create_batch(10)

        req = self.client.get('/api/categories')
        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(len(categories), len(req.json()))

    def test_category_update_category_name_not_ok(self):
        category = CategoryFactory()

        url = reverse('tellme:UpdateCategory', kwargs={'id': 0})

        request_should_return_404 = self.client.patch(path=url, data={'name': 'People', }, format='json')

        with patch.object(UpdateCategory, "get_queryset", return_value=Category.objects.none()) as mock_method:
            request_2_should_return_404 = self.client.patch(path=reverse('tellme:UpdateCategory', kwargs={'id': 0}), data={'name': 'People', }, format='json')

        view = UpdateCategory.as_view(permission_classes=(permissions.IsAuthenticated,))
        request = self.factory.patch(url, data={'id': category.id}, format='json')
        response_should_return_403 = view(request)

        mock_method.assert_called()
        self.assertEqual(request_should_return_404.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(request_2_should_return_404.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_should_return_403.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(category.name, Category.objects.filter(pk=category.id).first().name)

    def test_category_update_category_name_should_return_200(self):
        category = CategoryFactory.create_batch(2)
        url = reverse('tellme:UpdateCategory', kwargs={'id': category[0].id})
        request_1 = self.client.patch(url, {'name': 'People'}, format='json')

        user = User.objects.create_user('jab', password='test_password')
        view = UpdateCategory.as_view(permission_classes=(permissions.IsAuthenticated,))

        url = reverse('tellme:UpdateCategory', kwargs={'id': category[-1].id})
        request = self.factory.patch(url, data={'name': 'People 2'}, format='json')
        force_authenticate(request, user=user)
        second_request = view(request, id=category[-1].id)

        self.assertEqual(request_1.json()['name'], 'People')
        self.assertEqual(request_1.status_code, status.HTTP_200_OK)
        self.assertEqual(second_request.status_code, status.HTTP_200_OK)
        self.assertEqual(second_request.data['name'], 'People 2')

    def test_category_destroy_should_return_status_400_dont_delete(self):
        url = reverse('tellme:DeleteCategory')
        category = CategoryFactory()

        request_should_return_404 = self.client.delete(url, data={'id': 0}, format='json')

        with patch.object(DeleteCategory, "get_queryset", return_value=Category.objects.none()) as mock_method:
            req_should_return_404 = self.client.delete(path=url, data={'id': category.id}, format='json')

        view = DeleteCategory.as_view(permission_classes=(permissions.IsAuthenticated,))
        request = self.factory.delete(url, data={'id': category.id}, format='json')
        response_should_return_403 = view(request)

        mock_method.assert_called()
        self.assertEqual(request_should_return_404.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(req_should_return_404.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_should_return_403.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.all().count(), 1)

    def test_category_destroy_should_return_204_delete(self):
        category = CategoryFactory.create_batch(5)
        url = reverse('tellme:DeleteCategory')
        first_request = self.client.delete(url, {'id': category[0].id}, format='json')

        with patch.object(DeleteCategory, "get_object", return_value=category[-1]) as mock_method:
            second_request = self.client.delete(path=url, data={'id': 0}, format='json')

        user = User.objects.create_user('jab', password='test_password')

        view = DeleteCategory.as_view(permission_classes=(permissions.IsAuthenticated,))
        request = self.factory.delete(url, data={'id': category[1].id}, format='json')
        force_authenticate(request, user=user)
        third_request = view(request)

        mock_method.assert_called()
        self.assertEqual(first_request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(second_request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(third_request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.filter(pk=category[0].id).exists(), False)
        self.assertEqual(Category.objects.filter(pk=category[-1].id).exists(), False)
        self.assertEqual(Category.objects.filter(pk=category[1].id).exists(), False)
        self.assertEqual(Category.objects.all().count(), 2)
