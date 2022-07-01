import functools

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from tellme.models import Category
import factory
from faker import Faker

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'Category-{}'.format(n))
    description = factory.Faker('text')


def create_random_categories(count, **kwargs):
    category_list = []
    for i in range(0, count):
        cat = CategoryFactory(**kwargs)
        category_list.append(cat)

    return category_list


class CategoryTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_category_creation_ok(self):
        req = self.client.post('/api/category/', {
            'name': 'Animals',
            'description': fake.text()
        }, format='json')
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.filter(pk=req.json()['id']).exists(), True)

    def test_category_creation_not_ok(self):
        post = functools.partial(self.client.post, path='/api/category/', data={'description': fake.text()},
                                 format='json')
        get = functools.partial(self.client.get, path='/api/category/', data={'description': fake.text()},
                                format='json')

        self.assertEqual(post().status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(post(path='/api/categories/').status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get().status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_category_retrieve_ok_200(self):
        categories = create_random_categories(10)

        req = self.client.get('/api/categories')
        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(len(categories), len(req.json()))

    def test_category_update_category_name_ok(self):
        category = CategoryFactory()

        req = self.client.patch('/api/category/{}/'.format(category.id), {
            'name': 'People',
        }, format='json')
        self.assertEqual(req.json()['name'], 'People')
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def test_category_update_category_name_not_ok(self):
        patch = functools.partial(self.client.patch, path='/api/category/{}/'.format(0), data={'name': 'People', },
                                  format='json')
        get = functools.partial(self.client.get, path='/api/category/{}/'.format(0), data={'description': fake.text()},
                                format='json')

        self.assertEqual(patch().status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get().status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_category_destroy_not_ok(self):
        delete = functools.partial(self.client.delete, path='/api/category/remove/', data={'id': 0}, format='json')
        get = functools.partial(self.client.get, path='/api/category/remove/', data={'id': 0}, format='json')

        self.assertEqual(delete().status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(delete(path='/api/category/remove').status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.assertEqual(get().status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_category_destroy_ok(self):
        category = CategoryFactory()

        req = self.client.delete('/api/category/remove/', {'id': category.id}, format='json')

        self.assertEqual(req.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.filter(pk=category.id).exists(), False)
