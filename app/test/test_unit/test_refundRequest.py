from django.test import TestCase
from django.contrib.auth.models import User
from app.models import RefundRequest

class RefundRequestModelTest(TestCase):

    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="contrasenia123"
        )

    # ---------- VALIDATE ----------

    def test_validate_with_valid_data(self):
        errors = RefundRequest.validate(
            user=self.user,
            ticket_code="TICKET123",
            reason="No puedo asistir"
        )
        self.assertEqual(errors, {})

    def test_validate_with_empty_ticket_code(self):
        errors = RefundRequest.validate(
            user=self.user,
            ticket_code="",
            reason="Motivo válido"
        )
        self.assertIn("ticket_code", errors)
        self.assertEqual(errors["ticket_code"], "El codigo de la solicitud es obligatorio")

    def test_validate_with_empty_reason(self):
        errors = RefundRequest.validate(
            user=self.user,
            ticket_code="TICKET123",
            reason=""
        )
        self.assertIn("reason", errors)
        self.assertEqual(errors["reason"], "El motivo de la solicitud es obligatorio")

    def test_validate_with_no_user(self):
        errors = RefundRequest.validate(
            user=None,
            ticket_code="TICKET123",
            reason="Motivo válido"
        )
        self.assertIn("user", errors)
        self.assertEqual(errors["user"], "El usuario de la solicitud es obligatorio")

    # ---------- Tests de new ----------

    def test_new_with_valid_data(self):
        success, errors = RefundRequest.new(
            user=self.user,
            ticket_code="TICKET123",
            reason="No puedo asistir"
        )
        self.assertTrue(success)
        self.assertIsNone(errors)

        refund = RefundRequest.objects.get(ticket_code="TICKET123")
        self.assertEqual(refund.reason, "No puedo asistir")
        self.assertEqual(refund.user, self.user)
        self.assertFalse(refund.approved)
        self.assertFalse(refund.rejected)
        self.assertFalse(refund.resolved)

    def test_new_with_invalid_data(self):
        success, errors = RefundRequest.new(
            user=None,
            ticket_code="",
            reason=""
        )
        self.assertFalse(success)
        self.assertIn("user", errors)
        self.assertIn("ticket_code", errors)
        self.assertIn("reason", errors)