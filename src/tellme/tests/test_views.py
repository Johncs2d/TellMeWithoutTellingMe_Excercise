import io
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from src.services import FileHandlerService

from . import CategoryFactory
from src.containers import Container
from tellme.models import Item


class BytesIOWrapper:
    def __init__(self, string_buffer, encoding='utf-8'):
        self.string_buffer = string_buffer
        self.encoding = encoding

    def __getattr__(self, attr):
        return getattr(self.string_buffer, attr)

    def read(self, size=-1):
        content = self.string_buffer.read(size)
        return content.encode(self.encoding)

    def write(self, b):
        content = b.decode(self.encoding)
        return self.string_buffer.write(content)


def temporary_csv(name='text.csv'):
    bts = BytesIOWrapper(io.StringIO(
        """name
test1
test2
test3
test4"""
    ))
    return SimpleUploadedFile(name, bts.read(), content_type='text/csv')


class ViewTestCase(APITestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('http://localhost/')
        self.assertEqual(response.status_code, 200)

    def test_file_upload_handles_file_properly(self):
        category = CategoryFactory()
        client = APIClient()
        file = temporary_csv()
        url = reverse('tellme:uploadItems')

        file_handler_mock = mock.Mock(spec=FileHandlerService)
        file_handler_mock.read.return_value = [{'name': 'test1'}, {'name': 'test2'}, {'name': 'test3'}, {'name': 'test4'}]

        with Container.file_handler.override(file_handler_mock):
            req = client.post(url, {"file": file, "category": category.id})

        self.assertEqual(len(req.json()['data']), 4)
        self.assertEqual(Item.objects.all().count(), 4)