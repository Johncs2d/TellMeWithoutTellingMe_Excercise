from django.test import TestCase


class ViewTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('http://localhost/')
        self.assertEqual(response.status_code, 200)
