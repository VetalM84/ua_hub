"""Tests for HUB app."""
from unittest import skip

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
            start_coordinates="50.45, 30.52",
            avatar="avatar/default_avatar.jpg",
        )
        Icon.objects.create(name="cloud")
        Category.objects.create(name="Test category", icon_id=1, color="red")
        Marker.objects.create(
            pk=1,
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
        self.assertContains(
            response,
            text='<a class="dropdown-item" href="/logout/">Log out</a>',
            html=True,
        )

    def test_user_logout(self):
        """Test user log out with redirect to login page."""
        response = self.client.get(path=reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse("home"))

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

    def test_public_user_profile(self):
        """Test public user profile page."""
        url = reverse("public-profile", args=(User.objects.get(pk=1).id,))
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
            self.assertContains(response, text=field)

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
            id=2,
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

    def test_edit_marker_page(self):
        """Test edit marker page."""
        Marker.objects.create(
            latitude=32.6329,
            longitude=52.1747,
            category_id=1,
            comment="Test3 comment",
            owner=self.user,
            ip="127.0.0.3",
        )
        response = self.client.get(path=reverse("edit_marker", args=(2,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hub/edit-marker.html")
        self.assertContains(response, text="Test3 comment")

    def test_edit_foreign_marker(self):
        """Test edit foreign marker with exception raises."""
        with self.assertRaises(expected_exception=ValueError):
            self.client.get(path=reverse("edit_marker", args=(1,)))

    def test_edit_marker_post(self):
        """Test edit marker with post request."""
        Marker.objects.create(
            id=3,
            latitude=32.6329,
            longitude=52.1747,
            category_id=1,
            comment="Test3 comment",
            owner=self.user,
            ip="127.0.0.3",
        )
        response = self.client.post(
            path=reverse("edit_marker", args=(3,)),
            data={
                "latitude": 48.3544,
                "longitude": 31.9280,
                "comment": "Test Edit Marker",
                "category": 1,
                "owner": self.user.pk,
            },
            follow=True,
        )
        self.assertRedirects(response, expected_url=reverse("markers"))
        self.assertContains(response, text="Test Edit Marker")

    def test_change_password_page(self):
        """Test change password method page."""
        response = self.client.get(path=reverse("password_change"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/password/password_change.html")

    def test_change_password_success(self):
        """Test change password method page with success."""
        data = {
            "old_password": "test",
            "new_password1": "test_new_password",
            "new_password2": "test_new_password",
        }
        response = self.client.post(path=reverse("password_change"), data=data)
        self.assertRedirects(response, expected_url=reverse("profile"))

    def test_change_password_fail(self):
        """Test change password method page with wrong old password."""
        data = {
            "old_password": "test1111",
            "new_password1": "111111",
            "new_password2": "test_new_password",
        }
        response = self.client.post(path=reverse("password_change"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text=b'<div id="form_errors">')

    def test_get_marker(self):
        """Test single marker view page."""
        response = self.client.get(path=reverse("get_marker", args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hub/marker.html")

    def test_contact(self):
        """Test contact view page."""
        response = self.client.get(path=reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hub/contact.html")

    def test_contact_post(self):
        """Test contact form post method with success."""
        data = {
            "subject": "test subject",
            "message": "test message",
            "from_email": "from@email.co",
            "recipient_list": ["to@email.co"]
        }
        response = self.client.post(path=reverse("contact"), data=data)
        self.assertRedirects(response, expected_url=reverse("home"))

    def test_password_reset_page(self):
        """Test access to password reset page, check if it contains form."""
        response = self.client.get(path=reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/password/password_reset.html")
        self.assertContains(response, text='<input type="email"')

    def test_password_reset_post(self):
        """Test password reset post."""
        response = self.client.post(path=reverse("password_reset"), data={"email": "test@test.com"})
        self.assertRedirects(response, expected_url=reverse("home"))


class ViewsWithNoUserLoggedInTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_access_user_markers_page(self):
        """Test access to user markers page with redirect for non-logged-in users."""
        response = self.client.get(path=reverse("markers"))
        self.assertEqual(response.status_code, 302)

    def test_access_user_profile_page(self):
        """Test access to user profile page with redirect for non-logged-in users."""
        response = self.client.get(path=reverse("profile"))
        self.assertEqual(response.status_code, 302)

    def test_access_edit_marker_page(self):
        """Test access to user edit marker page with redirect for non-logged-in users."""
        url = reverse("edit_marker", args=(1,))
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 302)

    def test_user_register_page(self):
        """Test user register page."""
        response = self.client.get(path=reverse("register"))
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "inc/_header.html")
        self.assertTemplateUsed(response, "accounts/register.html")

        self.assertEqual(response.status_code, 200)
        fields = [
            'id="id_email"',
            'id="id_password1"',
            'id="id_password2"',
        ]
        for field in fields:
            self.assertContains(response, text=field)

    def test_user_register_post(self):
        """Test user register post data."""
        data = {
            "email": "test222@test.com",
            "password1": "i2Cmb3xnpC69",
            "password2": "i2Cmb3xnpC69",
        }
        response = self.client.post(path=reverse("register"), data=data, follow=True)
        self.assertRedirects(response, expected_url=reverse("profile"))

        self.assertContains(response, text="test222@test.com")
        self.assertContains(
            response,
            text=b'<div class="alert alert-success success alert-dismissible fade show" role="alert">',
        )

    def test_user_login_page(self):
        """Test user login page."""
        response = self.client.get(path=reverse("login"))
        self.assertEqual(response.status_code, 200)
        fields = [
            'id="id_username"',
            'id="id_password"',
            'type="submit"',
        ]
        for field in fields:
            self.assertContains(response, text=field)

    def test_user_login_post_fails(self):
        """Test user login post data with fails due to user not exists."""
        data = {
            "username": "test222@test.com",
            "password": "i2Cmb3xnpC69",
        }
        response = self.client.post(path=reverse("login"), data=data, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertContains(
            response,
            text=b'<div class="alert alert-danger error alert-dismissible fade show" role="alert">',
        )

    def test_user_login_post_success(self):
        """Test user login post data."""
        User.objects.create_user(
            email="test222@test.com",
            password="i2Cmb3xnpC69",
            first_name="TestFirstName",
            last_name="TestLastName",
            hometown="Kiev",
            facebook_link="https://www.facebook.com/profile.php?id=1000",
            contacts="+380991111111",
            avatar="avatar/default_avatar.jpg",
        )

        data = {
            "username": "test222@test.com",
            "password": "i2Cmb3xnpC69",
        }
        response = self.client.post(path=reverse("login"), data=data, follow=True)
        self.assertRedirects(response, expected_url=reverse("markers"))

    def test_password_change(self):
        """Test access to password change page with redirect for non-logged-in users."""
        response = self.client.get(path=reverse("password_change"))
        self.assertEqual(response.status_code, 302)
