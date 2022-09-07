"""Tests for HUB app."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.hub.models import Category, Color, Icon, Marker


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(email="test@test.com", password="test")
        Icon.objects.create(name="cloud")
        Color.objects.create(name="red")
        Category.objects.create(name="Test category", icon_id=1, color_id=1)
        Marker.objects.create(
            latitude=30.6329,
            longitude=50.1747,
            category_id=1,
            comment="Test comment",
            owner=None,
            ip="127.0.0.1",
        )
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")

    def setUp(self):
        self.user = User.objects.get(email="test@test.com")
        self.client.force_login(user=self.user)
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_user_logged_in(self):
        """Check that test user are logged in."""
        response = self.client.get(path=reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            text='<input type="hidden" id="owner" name="owner" value="1">',
            html=True,
        )

    def test_index(self):
        """Test home page."""
        response = self.client.get(path=reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_index_post(self):
        """Test post Marker request to home page."""
        response = self.client.post(
            path=reverse("home"),
            data={
                "latitude": 30.6329,
                "longitude": 50.1747,
                "comment": "comment",
                "category": 1,
                "owner": 1,
            },
            follow=True,
        )
        self.assertEqual(Marker.objects.all().count(), 2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
