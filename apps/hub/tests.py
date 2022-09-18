"""Tests for HUB app."""

from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.hub.models import Category, Icon, Marker


class ViewsWithLoggedInUserTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="TestFirstName",
            last_name="TestLastName",
            hometown="Kiev",
            facebook_link="https://www.facebook.com/profile.php?id=1000",
            contacts="+380991111111",
            avatar="src='/media/avatar/test_avatar.jpg'",
        )
        Icon.objects.create(name="cloud")
        Category.objects.create(name="Test category", icon_id=1, color="red")
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

    def test_index(self):
        """Test home page."""
        response = self.client.get(path=reverse("home"))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "inc/_header.html")
        self.assertTemplateUsed(response, "hub/index.html")

        # check for Add marker button popup form
        self.assertContains(response, text='name="addMarkerForm"')
        # check for a map rendered
        self.assertContains(response, text="center: [50.45, 30.52],")

    def test_user_logged_in(self):
        """Check that test user are logged in."""
        response = self.client.get(path=reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="/media/avatar/test_avatar.jpg")
        self.assertContains(
            response,
            text='<a class="dropdown-item" href="/logout/">Log out</a>',
            html=True,
        )

    def test_user_logout(self):
        """Test user log out with redirect to login page."""
        response = self.client.get(path=reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse("login"))

    def test_index_post(self):
        """Test post Marker request to home page."""
        response = self.client.post(
            path=reverse("home"),
            data={
                "latitude": 48.3544,
                "longitude": 31.9280,
                "comment": "comment",
                "category": 1,
                "owner": 1,
            },
            follow=True,
        )
        self.assertEqual(Marker.objects.all().count(), 2)
        self.assertEqual(Marker.objects.filter(owner_id=1).count(), 1)
        self.assertEqual(response.status_code, 200)

        # check if there is a marker on a map
        self.assertContains(response, text="[48.3544, 31.928]")
        # check if there is a Popup windows with user logged in
        self.assertContains(response, text="profile-public/1/")

    def test_lang_change(self):
        """Test language change."""
        response = self.client.post(
            path="/i18n/setlang/", data={"language": "ru"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='<html lang="ru">')

    def test_about_page(self):
        """Test about page."""
        response = self.client.get(path=reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hub/about.html")
        # check for Add marker button popup form
        self.assertNotContains(response, text='name="addMarkerForm"')

    def test_public_user_profile(self):
        """Test public user profile page."""
        # url = reverse("public-profile", args=(User.objects.get(pk=1).id,))
        url = reverse("public-profile", args=(1,))
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="TestFirstName TestLastName")
        self.assertTemplateUsed(response, "accounts/profile-public.html")

    def test_user_profile_update_form(self):
        """Test user profile page with update data form."""
        response = self.client.get(path=reverse("profile"))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "accounts/profile.html")

        self.assertContains(response, text="TestFirstName")
        self.assertContains(
            response,
            text=b'<form method="POST" id="user_update_form" enctype="multipart/form-data">',
        )
        fields = [
            'id="id_first_name"',
            'id="id_last_name"',
            'id="id_hometown"',
            'id="id_email"',
            'id="id_facebook_link"',
            'id="id_contacts"',
            'id="id_avatar"',
        ]
        for field in fields:
            self.assertContains(
                response,
                text=field,
            )

    def test_user_profile_update(self):
        """Test user profile update data."""
        data = {"first_name": "TestUpdateFirstName"}
        response = self.client.post(path=reverse("profile"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="TestUpdateFirstName")

    def test_user_markers_page(self):
        """Test user markers list page."""
        Marker.objects.create(
            latitude=31.6329,
            longitude=51.1747,
            category_id=1,
            comment="Test2 comment",
            owner=self.user,
            ip="127.0.0.2",
        )
        response = self.client.get(path=reverse("markers"))
        self.assertEqual(Marker.objects.filter(owner=self.user).count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hub/markers.html")

        self.assertContains(response, text="Test category")
        self.assertContains(response, text="Test2 comment")

    def test_user_markers_delete(self):
        """Test user markers delete."""
        Marker.objects.create(
            latitude=31.6329,
            longitude=51.1747,
            category_id=1,
            comment="Test2 comment",
            owner=self.user,
            ip="127.0.0.2",
        )
        response = self.client.post(path=reverse("markers"), data={"delete": 2})
        self.assertRedirects(response, expected_url=reverse("markers"))
        self.assertEqual(Marker.objects.filter(owner=self.user).count(), 0)
        print(response.content)
        # TODO: edit marker, edit foreign marker (access restr.)

    def test_change_password(self):
        """Test change password method page."""
        pass
