from django.test import TestCase
from django.urls import reverse, resolve

class TestUrls:
    def test_detail_urls(self):
        path = reverse('description', kwargs={'pk': 1})
        assert resolve(path).view_name == 'description'
