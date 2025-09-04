from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_login_success(self):
        url = reverse("login")
        data = {"username": "testuser", "password": "12345"}
        response = self.client.post(url, data)

       
        self.assertEqual(response.status_code, 302)
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_fail_wrong_password(self):
        url = reverse("login")
        data = {"username": "testuser", "password": "wrongpass"}
        response = self.client.post(url, data)

        # login incorrecto vuelve al formulario
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
