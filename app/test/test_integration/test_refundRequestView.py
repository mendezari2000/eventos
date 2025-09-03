import pytest
from django.urls import reverse
from app.models import Ticket, RefundRequest
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestRefundRequestView:

    def test_user_can_request_refund(self, client):
        # Crear usuario y ticket
        user = User.objects.create_user(username="matias", password="1234")
        ticket = Ticket.objects.create(
            quantity=1,
            type_ticket="GENERAL",
            prize=100,
            total=100,
            user=user
        )

        client.login(username="matias", password="1234")

        url = reverse("refund_request", kwargs={"ticket_id": ticket.id})
        response = client.post(url)

        assert response.status_code == 302  # Redirección tras éxito
        assert RefundRequest.objects.filter(ticket=ticket, user=user).exists()

    def test_cannot_refund_other_users_ticket(self, client):
        # Usuario dueño del ticket
        user2 = User.objects.create_user(username="usuario2", password="1234")
        ticket = Ticket.objects.create(
            quantity=1,
            type_ticket="GENERAL",
            prize=200,
            total=200,
            user=user2
        )

        # Otro usuario
        other_user = User.objects.create_user(username="intruso", password="1234")
        client.login(username="intruso", password="1234")

        url = reverse("refund_request", kwargs={"ticket_id": ticket.id})
        response = client.post(url)

        assert response.status_code == 403  # Forbidden
        assert not RefundRequest.objects.filter(ticket=ticket).exists()

    def test_cannot_refund_nonexistent_ticket(self, client):
        user = User.objects.create_user(username="test", password="1234")
        client.login(username="test", password="1234")

        url = reverse("refund_request", kwargs={"ticket_id": 999})
        response = client.post(url)

        assert response.status_code == 404
