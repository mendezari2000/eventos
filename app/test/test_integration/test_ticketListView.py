import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from app.models import Ticket, Event, Venue, Category, RefundRequest

class TicketListViewTest(TestCase):

    def setUp(self):
        # Crear usuario y loguearlo
        self.user = User.objects.create_user(
            username="usuario1",
            password="contrasenia123"
        )
        self.client.login(username="usuario1", password="contrasenia123")

        # Otro usuario para probar que no se muestren sus tickets
        self.user2 = User.objects.create_user(
            username="usuario2",
            password="123456"
        )

        # Venue y categoría
        self.venue = Venue.objects.create(
            name="Sala Principal",
            address="Calle Falsa 123",
            city="Ushuaia",
            capacity=100,
            contact="contacto@correo.com"
        )
        self.category = Category.objects.create(
            name="Musica",
            description="Eventos musicales",
            is_active=True
        )

        # Crear un evento pasado (para pruebas de reembolso)
        self.event = Event.objects.create(
            title="Concierto pasado",
            description="Evento pasado",
            date=timezone.now() - timedelta(days=1),
            venue=self.venue,
            category=self.category,
            prize=100
        )

        # Tickets del usuario 1
        self.ticket1 = Ticket.objects.create(
            user=self.user,
            event=self.event,
            quantity=2,
            type_ticket="GENERAL",
            prize=100,
            total=200,
            ticket_code=str(uuid.uuid4())[:8] 
        )

        # Ticket de otro usuario (no debería aparecer)
        self.ticket2 = Ticket.objects.create(
            user=self.user2,
            event=self.event,
            quantity=1,
            type_ticket="GENERAL",
            prize=100,
            total=100,
            ticket_code=str(uuid.uuid4())[:8] 
        )

        # Solicitud de reembolso pendiente
        self.refund = RefundRequest.objects.create(
            user=self.user,
            ticket_code=self.ticket1.ticket_code,
            reason="No puedo asistir",
            resolved=False
        )

    def test_ticket_list_view_muestra_tickets_del_usuario(self):
        url = reverse("tickets")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Solo tickets del usuario logueado
        tickets = response.context["tickets"]
        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0], self.ticket1)

        # Verificar total calculado correctamente
        self.assertEqual(tickets[0].total, 200)

        # Verificar bandera de reembolso pendiente
        self.assertTrue(tickets[0].refund_pending)
        self.assertFalse(hasattr(tickets[0], "refund_status"))
