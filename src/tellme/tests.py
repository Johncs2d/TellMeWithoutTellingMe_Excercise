from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
# Create your tests here.
from .models import Category, Item


class AccountTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def testCreateCategory(self):
        req = self.client.post('/api/category/', {
            'name': 'Animals',
        }, format='json')
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)

    def testUpdateCategory(self):
        instance = Category.objects.create(
            name = 'Test'
        )
        req = self.client.patch('/api/category/{}/'.format(instance.id), {
            'name': 'Test 1',
        }, format='json')
        self.assertEqual(req.json()['name'], 'Test 1')
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def testDeleteCategory(self):
        instance = Category.objects.create(
            name = 'Animals'
        )
        req = self.client.delete('/api/category/remove/',{
            'id': instance.id,
        }, format='json')

        self.assertEqual(req.status_code, status.HTTP_204_NO_CONTENT)

    def testRetrieveCategory(self):
        req = self.client.get('/api/categories')
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def testCreateItem(self):
        instance = Category.objects.create(
            name = 'Places'
        )

        req = self.client.post('/api/item/', {
            'name': 'Manila',
            'category': instance.id
        }, format='json')
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)
        self.assertEqual(req.json()['category'], instance.id)

    def testUpdateItem(self):
        instance = Category.objects.create(
            name = 'Places'
        )
        item_instance = Item.objects.create(
            name = 'Manila',
            category=instance
        )

        req = self.client.patch('/api/item/{}/'.format(item_instance.id), {
            'name': 'Manila Zoo',
        }, format='json')
        self.assertEqual(req.json()['name'], 'Manila Zoo')
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def testDeleteItem(self):
        instance = Category.objects.create(
            name = 'Places'
        )
        Item.objects.create(
            name = 'Manila',
            category=instance
        )

        item2_instance = Item.objects.create(
            name = 'Davao',
            category=instance
        )

        req = self.client.delete('/api/item/remove/',{
            'id': item2_instance.id,
        }, format='json')

        self.assertEqual(req.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.all().count(), 1)

    def testRetrieveCategoryItems(self):
        instance = Category.objects.create(
            name = 'Places'
        )

        Item.objects.create(
            name = 'Manila',
            category=instance
        )

        Item.objects.create(
            name = 'Davao',
            category=instance
        )

        req = self.client.get('/api/item/{}'.format(instance.id))
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def testRetrieveItemToGuess(self):
        instance = Category.objects.create(
            name = 'Places'
        )

        Item.objects.create(
            name = 'Manila',
            category=instance
        )

        Item.objects.create(
            name = 'Davao',
            category=instance
        )

        req = self.client.get('/api/item/guess/{}'.format(instance.id))
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def testSubmitScore(self):
        instance = Category.objects.create(
            name = 'Places'
        )
        req = self.client.post('/api/score/', {
            'category': instance.id,
            'name': 'JAB',
            'time': 10,
            'answer': 'Dog'
        }, format='json')

        self.assertEqual(req.status_code, status.HTTP_201_CREATED)