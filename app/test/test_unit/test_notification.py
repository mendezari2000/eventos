from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Notification, Priority


class NotificationModelTest(TestCase):
    def setUp(self):
        # Se crean usuarios de prueba
        self.user1 = User.objects.create_user(username="user1", password="contrasenia123")
        self.user2 = User.objects.create_user(username="user2", password="contrasenia123")

    # ---- VALIDATE ----
    def test_validate_with_valid_data(self):
        errors = Notification.validate("Título válido", "Mensaje válido", Priority.HIGH)
        self.assertEqual(errors, {})

    def test_validate_with_empty_title(self):
        errors = Notification.validate("", "Mensaje válido", Priority.LOW)
        self.assertIn("title", errors)

    def test_validate_with_empty_message(self):
        errors = Notification.validate("Título válido", "", Priority.MEDIUM)
        self.assertIn("message", errors)

    def test_validate_with_invalid_priority(self):
        errors = Notification.validate("Título válido", "Mensaje válido", "INVALID")
        self.assertIn("priority", errors)

    # ---- NEW ----
    def test_new_with_valid_data(self):
        success, errors = Notification.new(
            title="Nueva notificación",
            message="Este es un mensaje",
            priority=Priority.HIGH,
            users=[self.user1, self.user2]
        )

        self.assertTrue(success)
        self.assertIsNone(errors)

        notif = Notification.objects.get(title="Nueva notificación")
        self.assertEqual(notif.message, "Este es un mensaje")
        self.assertEqual(notif.priority, Priority.HIGH)
        self.assertEqual(notif.users.count(), 2)

    def test_new_with_invalid_data(self):
        success, errors = Notification.new(
            title="",
            message="",
            priority="INVALID",
            users=[self.user1]
        )

        self.assertFalse(success)
        self.assertIn("title", errors)
        self.assertIn("message", errors)
        self.assertIn("priority", errors)
