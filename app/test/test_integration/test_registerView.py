from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegisterViewTests(TestCase):
    def test_create_user(self):
        url = reverse("register")
        data = {
            "username": "nuevo_user",
            "password1": "Pass12345",
            "password2": "Pass12345",
        }

        response = self.client.post(url, data)

        # Verifica que redirige correctamente
        self.assertEqual(response.status_code, 302)

        # Verifica usuario creado en la base de datos
        self.assertTrue(User.objects.filter(username="nuevo_user").exists())

    def test__duplicate_username(self):
        User.objects.create_user(username="nuevo_user", password="12345")
        url = reverse("register")
        data = {
             "username": "nuevo_user",
             "password1": "Pass12345",
             "password2": "Pass12345",
            }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="nuevo_user").count(), 1)
