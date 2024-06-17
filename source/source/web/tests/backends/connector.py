from django.test import TestCase

from web.backends.connector import ApiConnector


class TestApiConnector(TestCase):
    def test_invalid_url(self):
        url = 'http://invalid-url'
        status, content = ApiConnector().get(url)
        self.assertEqual(400, status)

    def test_valid_url(self):
        url = 'https://www.djangoproject.com/start/overview/'
        status, content = ApiConnector().get(url)
        self.assertEqual(200, status)
