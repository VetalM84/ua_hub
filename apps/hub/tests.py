"""Tests for HUB app."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.hub.models import Marker


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_index(self):
        """Test home page with CarBrand list."""
        response = self.client.get(path=reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hub/index.html")
