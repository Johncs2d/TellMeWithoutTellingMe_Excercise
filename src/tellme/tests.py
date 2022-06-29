from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
# Create your tests here.
class AccountTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def testCreateCategory(self):
        req = self.client.post('/api/category/', {
            'name': 'Animals',
        }, format='json')
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)

    def testUpdateCategory(self):
        req = self.client.post('/api/category/', {
            'name': 'Test',
        }, format='json')
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)

        req = self.client.patch('/api/category/{}/'.format(req.json()['id']), {
            'name': 'Test 1',
        }, format='json')
        self.assertEqual(req.json()['name'], 'Test 1')
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def testDeleteCategory(self):
        req = self.client.post('/api/category/', {
            'name': 'Animals',
        }, format='json')
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)

        req = self.client.delete('/api/category/remove/',{
            'id': req.json()['id'],
        }, format='json')

        self.assertEqual(req.status_code, status.HTTP_204_NO_CONTENT)

    def testRetrieveCategory(self):
        req = self.client.get('/api/categories')
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def testCreateItem(self):

        req1 = self.client.post('/api/category/', {
            'name': 'Places',
        }, format='json')
        self.assertEqual(req1.status_code, status.HTTP_201_CREATED)

        req = self.client.post('/api/item/', {
            'name': 'Manila',
            'category': req1.json()['id']
        }, format='json')
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)
        self.assertEqual(req.json()['category'], req1.json()['id'])

    def testUpdateItem(self):
        req1 = self.client.post('/api/category/', {
            'name': 'Places',
        }, format='json')
        self.assertEqual(req1.status_code, status.HTTP_201_CREATED)

        req = self.client.post('/api/item/', {
            'name': 'Manila',
            'category': req1.json()['id']
        }, format='json')
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)
        self.assertEqual(req.json()['category'], req1.json()['id'])


        req = self.client.patch('/api/item/{}/'.format(req.json()['id']), {
            'name': 'Manila Zoo',
        }, format='json')
        self.assertEqual(req.json()['name'], 'Manila Zoo')
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def testDeleteItem(self):
        req1 = self.client.post('/api/category/', {
            'name': 'Places',
        }, format='json')
        self.assertEqual(req1.status_code, status.HTTP_201_CREATED)

        self.client.post('/api/item/', {
            'name': 'Manila',
            'category': req1.json()['id']
        }, format='json')

        req = self.client.post('/api/item/', {
            'name': 'Davao',
            'category': req1.json()['id']
        }, format='json')
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)
        self.assertEqual(req.json()['category'], req1.json()['id'])

        req = self.client.delete('/api/item/remove/',{
            'id': req.json()['id'],
        }, format='json')

        self.assertEqual(req.status_code, status.HTTP_204_NO_CONTENT)

    def testRetrieveCategoryItems(self):
        req1 = self.client.post('/api/category/', {
            'name': 'Places',
        }, format='json')
        self.assertEqual(req1.status_code, status.HTTP_201_CREATED)

        self.client.post('/api/item/', {
            'name': 'Manila',
            'category': req1.json()['id']
        }, format='json')

        req = self.client.post('/api/item/', {
            'name': 'Davao',
            'category': req1.json()['id']
        }, format='json')
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)
        self.assertEqual(req.json()['category'], req1.json()['id'])

        req = self.client.get('/api/item/{}'.format(req1.json()['id']))
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def testRetrieveItemToGuess(self):
        req1 = self.client.post('/api/category/', {
            'name': 'Places',
        }, format='json')
        self.assertEqual(req1.status_code, status.HTTP_201_CREATED)

        self.client.post('/api/item/', {
            'name': 'Manila',
            'category': req1.json()['id']
        }, format='json')

        req = self.client.post('/api/item/', {
            'name': 'Davao',
            'category': req1.json()['id']
        }, format='json')
        self.assertEqual(req.status_code, status.HTTP_201_CREATED)
        self.assertEqual(req.json()['category'], req1.json()['id'])

        req = self.client.get('/api/item/guess/{}'.format(req1.json()['id']))
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def testSubmitScore(self):
        req1 = self.client.post('/api/category/', {
            'name': 'Places',
        }, format='json')
        self.assertEqual(req1.status_code, status.HTTP_201_CREATED)

        req = self.client.post('/api/score/', {
            'category': req1.json()['id'],
            'name': 'JAB',
            'time': 10,
            'answer': 'Dog'
        }, format='json')
        print(req.json())
        self.assertEqual(req1.status_code, status.HTTP_201_CREATED)